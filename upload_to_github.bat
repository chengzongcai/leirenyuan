@echo off
echo 🚀 正在上传猿人学项目到GitHub...
echo.

echo 📋 请确保您已经在GitHub上创建了仓库: yuanrenxue-challenge-1
echo 🔗 GitHub仓库地址: https://github.com/YOUR_USERNAME/yuanrenxue-challenge-1
echo.

echo ⚠️  请将下面的YOUR_USERNAME替换为您的GitHub用户名，然后运行命令：
echo.

echo git remote add origin https://github.com/YOUR_USERNAME/yuanrenxue-challenge-1.git
echo git branch -M main
echo git push -u origin main
echo.

echo 📝 或者使用SSH（如果已配置SSH密钥）：
echo git remote add origin git@github.com:YOUR_USERNAME/yuanrenxue-challenge-1.git
echo git branch -M main
echo git push -u origin main
echo.

echo ✅ 上传完成后，您的项目将在以下地址可见：
echo https://github.com/YOUR_USERNAME/yuanrenxue-challenge-1
echo.

pause
