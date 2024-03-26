# attendance-system

出席管理システム

# 構築方法

※このコンテナは、Traefikコンテナが存在するrinサーバでのみ構築されます

1. クローン

```
git clone https://github.com/SLP-KBIT/attendance-system.git
```

2. ラズパイのIPアドレス、ユーザ名を``./app/scripts/getFile.sh``に記載する

3. SSH鍵を生成

```
ssh-keygen -q -t rsa -N '' -f ./app/key/attendance_key
```

4. 生成された``./app/key/attendance_key.pub``をラズパイ側の``./ssh/authorized_keys``として配置する

5. コンテナ構築

```
docker compose up -d
```