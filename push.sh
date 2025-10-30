#!/bin/bash
# ============================================
# 🚀 EVANGELION GitHub Auto Backup Script
# Made for KoreanKangstar
# ============================================

# 1. 프로젝트 폴더로 이동
cd ~/projects/evangelion || { echo "❌ 프로젝트 폴더를 찾을 수 없습니다."; exit 1; }

# 2. Git 사용자 정보 설정 (최초 1회만 필요)
git config user.name "KoreanKangstar"
git config user.email "kyhoon0828@dankook.ac.kr"

# 3. .gitignore 자동 생성 (민감 정보 제외)
cat > .gitignore <<EOF
__pycache__/
*.pyc
.env
config.json
credentials.json
*.db
*.sqlite3
*.log
instance/
*.pem
*.key
*.crt
*.bak
EOF

# 4. Git 초기화 (처음 한 번만 필요)
if [ ! -d ".git" ]; then
    echo "🆕 Git 저장소 초기화 중..."
    git init
    git branch -M main
    git remote add origin https://github.com/KoreanKangstar/EVANGELION.git
fi

# 5. 변경사항 커밋 & 푸시
echo "📦 변경사항 커밋 및 푸시 중..."
git add .
git commit -m "Auto backup $(date '+%Y-%m-%d %H:%M:%S')" || echo "⚠️ 커밋할 변경사항 없음"
git push -u origin main

# 6. 완료 메시지
echo "✅ GitHub 업로드 완료! ($(date '+%Y-%m-%d %H:%M:%S'))"
