# IT News Digest — Auto-Generated Daily

ระบบดึงข่าว IT อัตโนมัติ สรุปด้วย Gemini AI แล้ว deploy เป็น HTML รายวันบน GitHub Pages

## ขั้นตอน Setup (ทำครั้งเดียว)

### 1. สร้าง GitHub Repository

1. ไปที่ [github.com/new](https://github.com/new)
2. ตั้งชื่อ repo เช่น `it-news-digest`
3. ตั้งเป็น **Public** (GitHub Pages ฟรีต้องเป็น Public)
4. กด **Create repository**

### 2. Upload โค้ดขึ้น GitHub

```bash
cd it-news-digest
git init
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/it-news-digest.git
git push -u origin main
```

### 3. รับ Gemini API Key

1. ไปที่ [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. กด **Create API key**
3. Copy key ไว้

### 4. ตั้ง Secret ใน GitHub

1. ไปที่ repo → **Settings** → **Secrets and variables** → **Actions**
2. กด **New repository secret**
3. Name: `GEMINI_API_KEY`
4. Value: วาง API key ที่ copy ไว้
5. กด **Add secret**

### 5. เปิด GitHub Pages

1. ไปที่ repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. กด **Save**

### 6. ทดสอบ Run ครั้งแรก

1. ไปที่ **Actions** tab
2. เลือก **Daily IT News Digest**
3. กด **Run workflow** → **Run workflow**
4. รอ 1-2 นาที แล้ว refresh
5. เข้าดูหน้าเว็บที่ `https://YOUR_USERNAME.github.io/it-news-digest`

## ตารางเวลา

ระบบจะรันอัตโนมัติทุกวัน **08:00 น. เวลาไทย**

## แหล่งข่าว

| Source | หมวด |
|--------|------|
| TechCrunch | IT ทั่วไป |
| The Verge | IT ทั่วไป |
| Ars Technica | IT ทั่วไป |
| MIT Technology Review | AI / ML |
| Hacker News | Developer |

## ค่าใช้จ่าย

- **Gemini API**: ฟรี (gemini-2.0-flash มี free tier 1,500 req/day)
- **GitHub Actions**: ฟรี (2,000 minutes/month สำหรับ Public repo)
- **GitHub Pages**: ฟรี

**รวม: $0/เดือน**
