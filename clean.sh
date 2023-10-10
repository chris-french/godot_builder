

cd godot
git clean --force
cd ..

rm -rf bin/*
rm config/logs/*
docker system prune -f

