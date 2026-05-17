# 🚀 Blazing Banner Grabber

> A friendly little tool that shakes hands with servers and asks "Who are you?"

## 🤔 What's This All About?

Ever wondered what's running on that server? What version of SSH? What web server? This tool does the digital equivalent of knocking on a server's door and reading the nameplate.

**In plain English:** It connects to servers, says "hello" in the right protocol language, and grabs the banner (the server's self-introduction).

## ✨ Features

- **Blazing fast** - Uses threading to scan multiple ports at once (because waiting is boring)
- **Friendly interface** - No cryptic commands, just clear prompts
- **Smart triggers** - Knows how to say "hello" to different services (SSH, HTTP, FTP, etc.)
- **Error handling** - Won't crash if you sneeze on the keyboard
- **Colorful output** - Because monochrome terminals are so 1980s

## 🎯 What You Can Do With It

- **Port scanning** - Check which common ports are open (20 most common ports, not all 65,000+)
- **Banner grabbing** - See what service and version is running
- **Service identification** - Automatically recognizes common services
- **Interactive selection** - Pick which port to dig deeper into

## 🛠️ What You Need

- Python 3.6 or higher
- An internet connection (for scanning remote hosts)
- Permission to scan the target (please be ethical!)

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/banner-grabber.git

# Move into the directory
cd banner-grabber

# Run it (no dependencies needed - uses only standard library!)
python banner_grabber.py
