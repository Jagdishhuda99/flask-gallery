import sqlite3
import pandas as pd

# Database से connect करें
conn = sqlite3.connect(r'd:\zxfsDGzfdsh\google_drive_gallery_full\users.db')

# किसी टेबल (जैसे users) से data पढ़ें
df = pd.read_sql_query("SELECT * FROM users", conn)

# Excel फ़ाइल में सेव करें
df.to_excel("users.xlsx", index=False)  # या path के साथ पूरा नाम दें

conn.close()

print("✅ Export हो गया Excel में: users.xlsx")
