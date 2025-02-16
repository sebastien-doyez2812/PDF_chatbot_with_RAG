import subprocess
import webbrowser
import time


populate = input("Do you want to repopulate the Vector Database? [y/n]\n -> ").lower().strip()
if populate == "y":
    subprocess.run(["python", "load_docs_VDB.py", "--reset"], capture_output=True)
elif populate !='n':
    raise ValueError("Please answer with n or y...")

print("[i] Launching the backend...")
subprocess.Popen(["python",  "backend.py"])
print("[+] Backend Ready.\n\n[i] Launching the frontend in...")

for i in range(3):
    print(3 - i)
    time.sleep(1)

webbrowser.open(f"file://C:/Users/doyez/Documents/PDF_chatbot_with_RAG/www/main_page.html")
print("[+] AI Agent ready.")