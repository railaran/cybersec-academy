"""Seed data dummy untuk CyberSec Academy.
Jalankan: python -m backend.seed   (dari root project)
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.course import Course
from app.models.lab import Lab
from app.models.quiz import Quiz, Question, Answer
from app.models.tool import CyberTool
from app.models.event import Event
from app.models.progress import UserProgress
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("Seeding...")

# ---------- USERS ----------
if db.query(User).count() == 0:
    users = [
        ("Admin Cyber", "admin@cybersec.id", "admin123", "admin"),
        ("Budi Santoso", "budi@cybersec.id", "student123", "student"),
        ("Siti Aminah", "siti@cybersec.id", "student123", "student"),
        ("Andi Wijaya", "andi@cybersec.id", "student123", "student"),
        ("Rina Kartika", "rina@cybersec.id", "student123", "student"),
    ]
    for name, email, pw, role in users:
        db.add(User(full_name=name, email=email, password=hash_password(pw),
                    role=role, is_active=True))
    db.commit()
    print(f"  + {len(users)} users")
else:
    print("  = users sudah ada, skip")

# ---------- COURSES ----------
if db.query(Course).count() == 0:
    courses = [
        ("Dasar Keamanan Siber", "general", "beginner", 12, 0, True,
         "Pengenalan CIA triad, ancaman dasar, dan praktik keamanan."),
        ("Web Application Hacking", "offensive", "intermediate", 20, 250000, True,
         "SQLi, XSS, CSRF, SSRF, dan teknik eksploitasi web modern."),
        ("Network Penetration Testing", "offensive", "intermediate", 25, 350000, True,
         "Scanning, enumeration, exploitation jaringan."),
        ("Digital Forensics", "forensics", "advanced", 30, 450000, True,
         "Investigasi disk, memori, dan artefak sistem."),
        ("Malware Analysis 101", "defensive", "advanced", 28, 500000, False,
         "Static dan dynamic analysis untuk malware."),
        ("OSINT Fundamentals", "general", "beginner", 10, 0, True,
         "Pengumpulan informasi dari sumber terbuka."),
        ("Reverse Engineering", "offensive", "advanced", 35, 550000, False,
         "Disassembly, debugging, dan patch binary."),
        ("Cryptography untuk Pentester", "defensive", "intermediate", 18, 200000, True,
         "Hash, symmetric, asymmetric, dan serangan kripto."),
        ("Cloud Security AWS", "defensive", "intermediate", 22, 400000, True,
         "IAM, S3, EC2 security best practices."),
    ]
    for title, cat, lvl, dur, price, pub, desc in courses:
        db.add(Course(title=title, category=cat, level=lvl, duration_hours=dur,
                      price=price, is_published=pub, description=desc))
    db.commit()
    print(f"  + {len(courses)} courses")
else:
    print("  = courses sudah ada, skip")

# ---------- LABS ----------
if db.query(Lab).count() == 0:
    labs = [
        ("SQL Injection Dasar", "web", "easy", 100, 30, "CTF{sqli_basic}",
         "Eksploitasi login form rentan SQLi untuk bypass autentikasi."),
        ("XSS Reflected", "web", "easy", 100, 30, "CTF{xss_reflected}",
         "Temukan celah XSS di parameter pencarian."),
        ("Command Injection", "web", "medium", 200, 45, "CTF{cmd_inject_42}",
         "Eksploitasi input form untuk eksekusi command."),
        ("Port Scanning Master", "network", "easy", 100, 30, "CTF{nmap_master}",
         "Scan target dan temukan service tersembunyi."),
        ("Privilege Escalation Linux", "network", "hard", 300, 60, "CTF{privesc_root}",
         "Naik dari user biasa ke root."),
        ("Memory Forensics", "forensics", "medium", 250, 45, "CTF{mem_forensics}",
         "Analisis dump memory untuk temukan flag."),
        ("RSA Common Modulus", "crypto", "medium", 200, 40, "CTF{rsa_crypto}",
         "Pecahkan RSA dengan serangan common modulus."),
        ("Subdomain Enumeration", "osint", "easy", 100, 30, "CTF{osint_sub}",
         "Temukan subdomain target dengan OSINT."),
        ("Binary Patch", "reveng", "hard", 300, 60, "CTF{rev_patch}",
         "Patch binary untuk bypass license check."),
    ]
    for title, cat, diff, pts, t, flag, desc in labs:
        slug = title.lower().replace(" ", "-")
        db.add(Lab(title=title, slug=slug, category=cat, difficulty=diff,
                   points=pts, time_limit_min=t, flag=flag, description=desc,
                   objective=desc, docker_image=f"ctf/{cat}:{diff}", is_active=True))
    db.commit()
    print(f"  + {len(labs)} labs")
else:
    print("  = labs sudah ada, skip")

# ---------- QUIZZES ----------
if db.query(Quiz).count() == 0:
    quiz_defs = [
        ("Dasar Keamanan Siber", "easy", 15, [
            ("Apa kepanjangan CIA triad?",
             [("Confidentiality, Integrity, Availability", True),
              ("Central Intelligence Agency", False),
              ("Cyber, Internet, Access", False),
              ("Cryptography, Identity, Authentication", False)]),
            ("Apa itu phishing?",
             [("Serangan social engineering via email/pesan palsu", True),
              ("Serangan DDoS", False),
              ("Teknik enkripsi", False),
              ("Firewall rule", False)]),
        ]),
        ("Web Security", "medium", 20, [
            ("Cara paling efektif cegah SQLi?",
             [("Prepared statements / parameterized queries", True),
              ("WAF saja", False),
              ("Hide error messages", False),
              ("Ganti password", False)]),
            ("XSS jenis apa yang disimpan di server?",
             [("Stored XSS", True), ("Reflected XSS", False),
              ("DOM XSS", False), ("Blind XSS", False)]),
        ]),
        ("Network Security", "medium", 20, [
            ("Port default SSH?",
             [("22", True), ("21", False), ("80", False), ("443", False)]),
            ("Protokol aman untuk web?",
             [("HTTPS", True), ("HTTP", False), ("FTP", False), ("Telnet", False)]),
        ]),
        ("Cryptography", "hard", 25, [
            ("Algoritma simetris?",
             [("AES", True), ("RSA", False), ("ECC", False), ("DH", False)]),
            ("Panjang key AES-256?",
             [("256 bit", True), ("128 bit", False), ("512 bit", False), ("1024 bit", False)]),
        ]),
    ]
    total_q = 0
    for title, diff, t, questions in quiz_defs:
        q = Quiz(title=title, difficulty=diff, time_limit_min=t,
                 description=f"Quiz {title}", category="general", is_active=True)
        db.add(q); db.flush()
        for i, (text, answers) in enumerate(questions):
            question = Question(quiz_id=q.id, text=text, type="single", points=1, order=i)
            db.add(question); db.flush()
            for a_text, a_correct in answers:
                db.add(Answer(question_id=question.id, text=a_text, is_correct=a_correct))
            total_q += 1
    db.commit()
    print(f"  + {len(quiz_defs)} quizzes ({total_q} questions)")
else:
    print("  = quizzes sudah ada, skip")

# ---------- TOOLS ----------
if db.query(CyberTool).count() == 0:
    tools = [
        ("Nmap", "recon", "linux", True, "sudo apt install nmap",
         "nmap -sV -p- target.com", "Port scanner & service detection"),
        ("Burp Suite", "web", "windows", False, "https://portswigger.net/burp",
         "Proxy intercept HTTP/HTTPS", "Web app security testing"),
        ("Metasploit", "exploitation", "linux", True, "curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall",
         "msfconsole", "Exploitation framework"),
        ("Wireshark", "network", "linux", True, "sudo apt install wireshark",
         "wireshark", "Packet analyzer"),
        ("John the Ripper", "crypto", "linux", True, "sudo apt install john",
         "john --wordlist=rockyou.txt hash.txt", "Password cracker"),
        ("Hashcat", "crypto", "linux", True, "sudo apt install hashcat",
         "hashcat -m 0 -a 0 hash.txt rockyou.txt", "GPU password cracker"),
        ("Gobuster", "recon", "linux", True, "go install github.com/OJ/gobuster/v3@latest",
         "gobuster dir -u http://target -w wordlist.txt", "Directory brute force"),
        ("ffuf", "recon", "linux", True, "go install github.com/ffuf/ffuf@latest",
         "ffuf -u http://target/FUZZ -w wordlist.txt", "Fast web fuzzer"),
        ("sqlmap", "web", "linux", True, "sudo apt install sqlmap",
         "sqlmap -u 'http://target/?id=1' --dbs", "SQL injection automation"),
        ("Nikto", "web", "linux", True, "sudo apt install nikto",
         "nikto -h http://target", "Web server scanner"),
        ("Volatility", "forensics", "linux", True, "pip install volatility3",
         "vol.py -f memory.dump windows.info", "Memory forensics"),
        ("Ghidra", "reveng", "linux", True, "https://ghidra-sre.org/",
         "ghidraRun", "Reverse engineering suite"),
        ("theHarvester", "osint", "linux", True, "sudo apt install theharvester",
         "theHarvester -d target.com -b google", "Email/subdomain OSINT"),
        ("Maltego", "osint", "linux", False, "https://www.maltego.com/",
         "maltego", "OSINT graph analysis"),
        ("Autopsy", "forensics", "windows", True, "https://www.autopsy.com/",
         "autopsy", "Disk forensics"),
        ("Aircrack-ng", "network", "linux", True, "sudo apt install aircrack-ng",
         "aircrack-ng capture.cap", "WiFi security auditing"),
    ]
    for name, cat, plat, oss, install, usage, desc in tools:
        db.add(CyberTool(name=name, category=cat, platform=plat,
                         is_open_source=oss, install_cmd=install,
                         usage_hint=usage, description=desc,
                         homepage="https://example.com/" + name.lower(),
                         is_active=True))
    db.commit()
    print(f"  + {len(tools)} tools")
else:
    print("  = tools sudah ada, skip")

# ---------- EVENTS ----------
if db.query(Event).count() == 0:
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    events = [
        ("CTF Beginner #1", "ctf", "Online", True, 0, 100, now + timedelta(days=7),
         now + timedelta(days=7, hours=6), "CTF untuk pemula, 10 soal web & crypto."),
        ("Workshop Burp Suite", "workshop", "Jakarta", False, 150000, 30,
         now + timedelta(days=14), now + timedelta(days=14, hours=8),
         "Workshop intensif Burp Suite dari dasar."),
        ("Webinar Karier Cyber Security", "webinar", "Online", True, 0, 500,
         now + timedelta(days=3), now + timedelta(days=3, hours=2),
         "Sharing karier di industri keamanan siber."),
        ("Bootcamp Ethical Hacking 4 Minggu", "bootcamp", "Bandung", False, 1500000, 20,
         now + timedelta(days=30), now + timedelta(days=58),
         "Bootcamp intensif 4 minggu, sertifikat."),
        ("CTF Intermediate #2", "ctf", "Online", True, 0, 150,
         now + timedelta(days=21), now + timedelta(days=21, hours=8),
         "CTF level medium, pwn & rev."),
        ("Workshop Digital Forensics", "workshop", "Surabaya", False, 250000, 25,
         now + timedelta(days=40), now + timedelta(days=40, hours=8),
         "Belajar forensics dari kasus nyata."),
    ]
    for title, typ, loc, free, price, cap, start, end, desc in events:
        slug = title.lower().replace(" ", "-").replace("#", "")
        db.add(Event(title=title, slug=slug, type=typ, location=loc,
                     is_free=free, price=price, capacity=cap,
                     start_at=start, end_at=end, description=desc,
                     is_published=True))
    db.commit()
    print(f"  + {len(events)} events")
else:
    print("  = events sudah ada, skip")

# ---------- PROGRESS (buat leaderboard ramai) ----------
if db.query(UserProgress).count() == 0:
    labs = db.query(Lab).all()
    quizzes = db.query(Quiz).all()
    students = db.query(User).filter(User.role == "student").all()
    for student in students:
        # setiap student selesaikan 2-5 lab & 1-3 quiz random
        for lab in random.sample(labs, k=min(len(labs), random.randint(2, 5))):
            db.add(UserProgress(user_id=student.id, item_type="lab",
                                item_id=lab.id, status="completed",
                                score=100, points=lab.points))
        for quiz in random.sample(quizzes, k=min(len(quizzes), random.randint(1, 3))):
            db.add(UserProgress(user_id=student.id, item_type="quiz",
                                item_id=quiz.id, status="completed",
                                score=random.randint(70, 100),
                                points=random.randint(50, 150)))
    db.commit()
    print(f"  + progress untuk {len(students)} students")
else:
    print("  = progress sudah ada, skip")

db.close()
print("✅ Seed selesai!")
print()
print("Login:")
print("  admin@cybersec.id / admin123    (admin)")
print("  budi@cybersec.id  / student123  (student)")
