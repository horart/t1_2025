# t1_2025
T1 hackathon 2025 HR Consultant

## Запуск
На Windows исполните следующую команду во избежание различия между форматами newline-символов, прежде чем делать `git clone`:
```
git config --global core.autocrlf false
```

### Первый запуск
```
RESTORE_DUMP=1 docker compose up
```
Также используйте, если хотите сбросить до исходного состояния

### Последующие запуски
```
docker compose up
```