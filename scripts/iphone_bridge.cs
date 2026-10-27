using System;
using System.Collections.Concurrent;
using System.IO;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public sealed class ReadyproofIphoneBridge : IDisposable
{
    readonly TcpListener tlsListener, certificateListener;
    readonly IPAddress allowedPhone;
    readonly int upstreamPort;
    readonly CancellationTokenSource stop = new CancellationTokenSource();
    readonly RSA serverKey;
    readonly X509Certificate2 serverCertificate;
    readonly byte[] publicCertificate;
    readonly Task tlsLoop, certificateLoop;
    readonly ConcurrentDictionary<int,TcpClient> clients = new ConcurrentDictionary<int,TcpClient>();
    int sequence, denied, tlsErrors;
    public int HttpsPort { get { return ((IPEndPoint)tlsListener.LocalEndpoint).Port; } }
    public int CertificatePort { get { return ((IPEndPoint)certificateListener.LocalEndpoint).Port; } }
    public int Denied { get { return Volatile.Read(ref denied); } }
    public int TlsErrors { get { return Volatile.Read(ref tlsErrors); } }
    public string CertificateSha256 { get { return Convert.ToHexString(SHA256.HashData(publicCertificate)); } }
    public byte[] PublicCertificate { get { return (byte[])publicCertificate.Clone(); } }

    public ReadyproofIphoneBridge(string address, string phone, int httpsPort, int certificatePort, int targetPort)
    {
        var local = IPAddress.Parse(address);
        allowedPhone = IPAddress.Parse(phone);
        if (local.AddressFamily != AddressFamily.InterNetwork || allowedPhone.AddressFamily != AddressFamily.InterNetwork)
            throw new ArgumentException("Se requiere IPv4 explícita.");
        upstreamPort = targetPort;
        serverKey = RSA.Create(3072);
        using (var caKey = RSA.Create(3072))
        {
            var caRequest = new CertificateRequest("CN=readyproof revision temporal", caKey, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
            caRequest.CertificateExtensions.Add(new X509BasicConstraintsExtension(true, true, 0, true));
            caRequest.CertificateExtensions.Add(new X509KeyUsageExtension(X509KeyUsageFlags.KeyCertSign | X509KeyUsageFlags.CrlSign, true));
            caRequest.CertificateExtensions.Add(new X509SubjectKeyIdentifierExtension(caRequest.PublicKey, false));
            var from = DateTimeOffset.UtcNow.AddMinutes(-5);
            var until = DateTimeOffset.UtcNow.AddHours(24);
            using (var ca = caRequest.CreateSelfSigned(from, until))
            {
                publicCertificate = ca.Export(X509ContentType.Cert);
                var request = new CertificateRequest("CN=readyproof prueba iPhone", serverKey, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
                request.CertificateExtensions.Add(new X509BasicConstraintsExtension(false, false, 0, true));
                request.CertificateExtensions.Add(new X509KeyUsageExtension(X509KeyUsageFlags.DigitalSignature | X509KeyUsageFlags.KeyEncipherment, true));
                var usage = new OidCollection(); usage.Add(new Oid("1.3.6.1.5.5.7.3.1"));
                request.CertificateExtensions.Add(new X509EnhancedKeyUsageExtension(usage, true));
                var names = new SubjectAlternativeNameBuilder(); names.AddIpAddress(local);
                request.CertificateExtensions.Add(names.Build());
                var serial = RandomNumberGenerator.GetBytes(16); serial[0] &= 0x7f; serial[0] |= 1;
                using (var leaf = request.Create(ca, from, until.AddMinutes(-1), serial))
                    serverCertificate = leaf.CopyWithPrivateKey(serverKey);
            }
        }
        tlsListener = new TcpListener(local, httpsPort);
        certificateListener = new TcpListener(local, certificatePort);
        try { tlsListener.Start(16); certificateListener.Start(8); }
        catch { tlsListener.Stop(); certificateListener.Stop(); serverCertificate.Dispose(); serverKey.Dispose(); throw; }
        tlsLoop = Accept(tlsListener, true);
        certificateLoop = Accept(certificateListener, false);
    }
    async Task Accept(TcpListener listener, bool tls)
    {
        while (!stop.IsCancellationRequested)
        {
            TcpClient client;
            try { client = await listener.AcceptTcpClientAsync(stop.Token).ConfigureAwait(false); }
            catch (OperationCanceledException) { break; }
            catch (SocketException) when (stop.IsCancellationRequested) { break; }
            if (!((IPEndPoint)client.Client.RemoteEndPoint).Address.Equals(allowedPhone))
            { Interlocked.Increment(ref denied); client.Dispose(); continue; }
            if (clients.Count >= 32) { client.Dispose(); continue; }
            int id = Interlocked.Increment(ref sequence); clients[id] = client;
            _ = Serve(client, id, tls);
        }
    }
    async Task Serve(TcpClient client, int id, bool tls)
    {
        try
        {
            if (tls) await Relay(client).ConfigureAwait(false);
            else await Certificate(client).ConfigureAwait(false);
        }
        catch (Exception) { if (tls) Interlocked.Increment(ref tlsErrors); }
        finally { TcpClient removed; clients.TryRemove(id, out removed); client.Dispose(); }
    }
    async Task Relay(TcpClient client)
    {
        using (var ssl = new SslStream(client.GetStream(), false))
        using (var timeout = CancellationTokenSource.CreateLinkedTokenSource(stop.Token))
        {
            timeout.CancelAfter(TimeSpan.FromSeconds(15));
            await ssl.AuthenticateAsServerAsync(new SslServerAuthenticationOptions {
                ServerCertificate = serverCertificate,
                EnabledSslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13,
                ClientCertificateRequired = false,
                CertificateRevocationCheckMode = X509RevocationMode.NoCheck,
                ApplicationProtocols = new System.Collections.Generic.List<SslApplicationProtocol>{ SslApplicationProtocol.Http11 }
            }, timeout.Token).ConfigureAwait(false);
            using (var upstream = new TcpClient(AddressFamily.InterNetwork))
            using (var session = CancellationTokenSource.CreateLinkedTokenSource(stop.Token))
            {
                session.CancelAfter(TimeSpan.FromMinutes(5));
                await upstream.ConnectAsync(IPAddress.Loopback, upstreamPort, session.Token).ConfigureAwait(false);
                var network = upstream.GetStream();
                Task sending = ssl.CopyToAsync(network, session.Token);
                Task receiving = network.CopyToAsync(ssl, session.Token);
                await Task.WhenAny(sending, receiving).ConfigureAwait(false);
                session.Cancel(); upstream.Close();
                try { await Task.WhenAll(sending, receiving).ConfigureAwait(false); }
                catch (OperationCanceledException) { }
                catch (IOException) { }
            }
        }
    }
    async Task Certificate(TcpClient client)
    {
        using (var timeout = CancellationTokenSource.CreateLinkedTokenSource(stop.Token))
        {
            timeout.CancelAfter(TimeSpan.FromSeconds(10));
            var stream = client.GetStream();
            var header = new MemoryStream(); var one = new byte[1]; string request = "";
            while (header.Length < 8192)
            {
                int n = await stream.ReadAsync(one, timeout.Token).ConfigureAwait(false);
                if (n == 0) return; header.WriteByte(one[0]);
                if (header.Length >= 4) {
                    var bytes = header.GetBuffer(); int l = (int)header.Length;
                    if (bytes[l-4]==13 && bytes[l-3]==10 && bytes[l-2]==13 && bytes[l-1]==10) {
                        request = Encoding.ASCII.GetString(bytes,0,l); break;
                    }
                }
            }
            bool download = request.StartsWith("GET /readyproof.cer HTTP/1.", StringComparison.Ordinal);
            bool home = request.StartsWith("GET / HTTP/1.", StringComparison.Ordinal);
            byte[] body; string type, status;
            if (download) { body=publicCertificate; type="application/x-x509-ca-cert"; status="200 OK"; }
            else if (home) {
                body=Encoding.UTF8.GetBytes("<!doctype html><html lang='es'><meta name='viewport' content='width=device-width'><meta charset='utf-8'><title>readyproof: certificado temporal</title><h1>Prueba local de readyproof</h1><p>Este acceso entrega solamente el certificado público de revisión. Compará esta huella con la informada en la computadora antes de instalarlo.</p><p>SHA256: <code>"+CertificateSha256+"</code></p><p><a href='/readyproof.cer'>Descargar certificado temporal</a></p><p>Instalalo en Ajustes y habilitá su confianza completa únicamente para esta prueba. Retiralo al terminar.</p></html>"); type="text/html; charset=utf-8"; status="200 OK";
            } else { body=Encoding.UTF8.GetBytes("Recurso no disponible."); type="text/plain; charset=utf-8"; status="404 Not Found"; }
            string headers="HTTP/1.1 "+status+"\r\nContent-Type: "+type+"\r\nContent-Length: "+body.Length+"\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n"+(download?"Content-Disposition: attachment; filename=readyproof-prueba.cer\r\n":"")+"\r\n";
            await stream.WriteAsync(Encoding.ASCII.GetBytes(headers),timeout.Token).ConfigureAwait(false);
            await stream.WriteAsync(body,timeout.Token).ConfigureAwait(false);
        }
    }
    public void Dispose()
    {
        stop.Cancel(); tlsListener.Stop(); certificateListener.Stop();
        foreach (var entry in clients) entry.Value.Dispose();
        try { Task.WhenAll(tlsLoop,certificateLoop).Wait(TimeSpan.FromSeconds(3)); } catch { }
        serverCertificate.Dispose(); serverKey.Dispose(); stop.Dispose();
    }
}
