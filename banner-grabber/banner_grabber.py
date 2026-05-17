import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Common ports that typically have banners
COMMON_PORTS = {
    21: "FTP",
    22: "SSH", 
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

# Triggers for different services (optimized)
TRIGGERS = {
    21: b"USER anonymous\r\n",
    22: b"\n",
    23: b"\n",
    25: b"HELO\r\n",
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    110: b"QUIT\r\n",
    143: b"CAPABILITY\r\n",
    443: b"HEAD / HTTP/1.0\r\n\r\n",
    8080: b"HEAD / HTTP/1.0\r\n\r\n",
}

def grab_banner(target, port, timeout=2):
    """Quick banner grab for a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        start = time.time()
        result = sock.connect_ex((target, port))
        connect_time = time.time() - start
        
        if result == 0:
            # Send trigger if available
            if port in TRIGGERS:
                sock.send(TRIGGERS[port])
            
            # Try to receive banner
            try:
                banner = sock.recv(256)  # Only need first 256 chars
                banner_text = banner.decode('utf-8', errors='ignore').strip().split('\n')[0]
            except:
                banner_text = "No banner (service may require authentication)"
            
            sock.close()
            return (port, True, banner_text, connect_time)
        else:
            sock.close()
            return (port, False, None, connect_time)
            
    except Exception:
        return (port, False, None, 0)

def fast_port_scan(target, ports=None, max_workers=50, timeout=2):
    """Blazing fast concurrent port scanning"""
    if ports is None:
        ports = list(COMMON_PORTS.keys())
    
    open_ports = []
    total = len(ports)
    
    print(f"\n[+] Scanning {len(ports)} common ports on {target}")
    print(f"[+] Using {max_workers} concurrent threads (timeout: {timeout}s)\n")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(grab_banner, target, port, timeout): port for port in ports}
        
        completed = 0
        for future in as_completed(futures):
            port, is_open, banner, conn_time = future.result()
            completed += 1
            
            if is_open:
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"  ✓ Port {port:5d} ({service:<10s}) - OPEN - {conn_time:.3f}s")
                open_ports.append((port, service, banner))
            else:
                # Optional: show closed ports (comment out for cleaner output)
                # print(f"  ✗ Port {port:5d} - CLOSED")
                pass
            
            # Show progress every 10 ports
            if completed % 10 == 0:
                print(f"  [~] Progress: {completed}/{total} ports", end='\r')
    
    elapsed = time.time() - start_time
    print(f"\n\n[+] Scan completed in {elapsed:.2f} seconds")
    print(f"[+] Found {len(open_ports)} open ports")
    
    return open_ports

def display_banner_art():
    """Display cool ASCII art banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    BLAZING BANNER GRABBER                    ║
    ║                     v1.0 - Lightning Fast                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def grab_full_banner(target, port, service, timeout=3):
    """Get complete banner from selected port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))
        
        # Send trigger
        if port in TRIGGERS:
            sock.send(TRIGGERS[port])
        
        # Receive banner
        banner_data = sock.recv(1024)
        banner_text = banner_data.decode('utf-8', errors='ignore').strip()
        
        sock.close()
        return banner_text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main interactive banner grabber"""
    display_banner_art()
    
    # Disclaimer
    print("[!] Disclaimer: Only use on systems you own or have permission to test\n")
    
    # Get target
    target = input("[?] Enter target IP or hostname: ").strip()
    
    if not target:
        print("[!] No target entered.")
        sys.exit(1)
    
    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(target)
        print(f"[+] Resolved: {target} → {target_ip}")
    except:
        print(f"[!] Could not resolve {target}")
        sys.exit(1)
    
    # Ask for speed preference
    print("\n[?] Speed options:")
    print("    1. Normal (2s timeout, 50 threads) - Balanced")
    print("    2. Fast (1s timeout, 100 threads) - For local networks")
    print("    3. Paranoid (5s timeout, 20 threads) - For slow networks")
    
    speed_choice = input("\n[?] Choose speed (1/2/3) [default: 1]: ").strip()
    
    if speed_choice == "2":
        timeout, workers = 1, 100
    elif speed_choice == "3":
        timeout, workers = 5, 20
    else:
        timeout, workers = 2, 50
    
    # Quick port scan (just common ports)
    print("\n" + "=" * 70)
    print(" PHASE 1: FAST PORT SCAN (Common Ports Only)")
    print("=" * 70)
    
    open_ports = fast_port_scan(target, timeout=timeout, max_workers=workers)
    
    if not open_ports:
        print(f"\n[!] No common open ports found on {target}")
        print("[!] Try scanning with a port scanner first, or the target may be down")
        sys.exit(1)
    
    # Banner grabbing phase
    print("\n" + "=" * 70)
    print(" PHASE 2: BANNER GRABBING")
    print("=" * 70)
    
    print(f"\n[+] Found {len(open_ports)} service(s) with banners:")
    print("-" * 70)
    
    for i, (port, service, quick_banner) in enumerate(open_ports, 1):
        # Show preview banner
        banner_preview = quick_banner[:50] + "..." if len(quick_banner) > 50 else quick_banner
        print(f"  {i}. Port {port} ({service})")
        print(f"     └─ {banner_preview}\n")
    
    # Let user choose which banner to grab in detail
    while True:
        try:
            print("-" * 70)
            choice = input(f"[?] Select port for detailed banner (1-{len(open_ports)}) or 'all': ").strip()
            
            if choice.lower() == 'all':
                print("\n[+] Grabbing detailed banners from all open ports...\n")
                for port, service, _ in open_ports:
                    print("=" * 70)
                    print(f" BANNER FROM PORT {port} ({service})")
                    print("=" * 70)
                    banner = grab_full_banner(target, port, service)
                    print(banner)
                    print()
                break
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(open_ports):
                    port, service, _ = open_ports[idx]
                    print("\n" + "=" * 70)
                    print(f" DETAILED BANNER - PORT {port} ({service})")
                    print("=" * 70)
                    print(f" Target: {target}:{port}")
                    print("-" * 70)
                    
                    banner = grab_full_banner(target, port, service)
                    print(f"\n{banner}\n")
                    print("=" * 70)
                    break
                else:
                    print(f"[!] Enter number between 1 and {len(open_ports)}")
        except ValueError:
            print("[!] Invalid input. Enter number or 'all'")
    
    print("\n[+] Banner grabbing completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)