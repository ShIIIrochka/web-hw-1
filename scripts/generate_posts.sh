#!/bin/bash

# Скрипт для создания 100 постов с моковыми данными
# Использование: ./scripts/generate_posts.sh [API_URL]

API_URL="${1:-http://localhost:8000}"

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Создание пользователя и получение токена...${NC}"

# Регистрация пользователя
REGISTER_RESPONSE=$(curl -s -X POST "${API_URL}/user/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@gmail.com",
    "login": "demo_user",
    "password": "demo123456"
  }')

# Проверка успешности регистрации
if echo "$REGISTER_RESPONSE" | grep -q '"access"'; then
  echo -e "${GREEN}✓ Пользователь зарегистрирован${NC}"
  TOKEN=$(echo "$REGISTER_RESPONSE" | sed -n 's/.*"access":"\([^"]*\)".*/\1/p')
elif echo "$REGISTER_RESPONSE" | grep -qi "already exists\|validation\|already registered"; then
  echo -e "${YELLOW}Пользователь уже существует, выполняется вход...${NC}"
  # Попытка входа
  LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/user/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "demo@example.com",
      "password": "demo123456"
    }')
  if echo "$LOGIN_RESPONSE" | grep -q '"access"'; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"access":"\([^"]*\)".*/\1/p')
  else
    echo -e "${RED}Ошибка при входе: $LOGIN_RESPONSE${NC}"
    exit 1
  fi
else
  echo -e "${RED}Ошибка при регистрации: $REGISTER_RESPONSE${NC}"
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo -e "${RED}Не удалось получить токен!${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Токен получен${NC}"

# Создание категорий
echo -e "${YELLOW}Создание категорий...${NC}"

CATEGORIES=("Технологии" "Наука" "Путешествия" "Еда" "Спорт" "Искусство" "Музыка" "Кино" "Книги" "Дизайн")
CATEGORY_IDS=()

for category_name in "${CATEGORIES[@]}"; do
  CATEGORY_RESPONSE=$(curl -s -X POST "${API_URL}/categories/create" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "{\"name\": \"${category_name}\"}")
  
  if echo "$CATEGORY_RESPONSE" | grep -q '"id"'; then
    CAT_ID=$(echo "$CATEGORY_RESPONSE" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')
    CATEGORY_IDS+=("$CAT_ID")
    echo -e "${GREEN}✓ Категория создана: ${category_name}${NC}"
  elif echo "$CATEGORY_RESPONSE" | grep -q "already exists"; then
    echo -e "${YELLOW}Категория уже существует: ${category_name}${NC}"
    # Попытка получить ID существующей категории через список
    CATEGORIES_LIST=$(curl -s -X GET "${API_URL}/categories?limit=100" \
      -H "Authorization: Bearer ${TOKEN}")
    CAT_ID=$(echo "$CATEGORIES_LIST" | grep -A1 "\"name\":\"${category_name}\"" | grep '"id"' | sed -n 's/.*"id":"\([^"]*\)".*/\1/p' | head -1)
    if [ -n "$CAT_ID" ]; then
      CATEGORY_IDS+=("$CAT_ID")
    fi
  else
    echo -e "${YELLOW}Не удалось создать категорию ${category_name}, продолжаем...${NC}"
  fi
done

if [ ${#CATEGORY_IDS[@]} -eq 0 ]; then
  echo -e "${YELLOW}Получение существующих категорий...${NC}"
  CATEGORIES_LIST=$(curl -s -X GET "${API_URL}/categories?limit=100" \
    -H "Authorization: Bearer ${TOKEN}")
  # Извлекаем все ID категорий
  while IFS= read -r line; do
    if [[ -n "$line" ]]; then
      CATEGORY_IDS+=("$line")
    fi
  done < <(echo "$CATEGORIES_LIST" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p' | head -10)
fi

echo -e "${GREEN}✓ Доступно категорий: ${#CATEGORY_IDS[@]}${NC}"

# Моковые заголовки и контент для постов
TITLES=(
  "Интересные факты о программировании"
  "10 способов улучшить продуктивность"
  "История развития веб-технологий"
  "Секреты эффективного обучения"
  "Как начать карьеру в IT"
  "Топ-5 инструментов для разработчиков"
  "Современные тренды в дизайне"
  "Путешествие по красивым местам"
  "Рецепты домашней кухни"
  "Спортивные достижения и рекорды"
  "Искусство фотографии"
  "Музыкальные новинки этого года"
  "Обзор новых фильмов"
  "Книги, которые стоит прочитать"
  "Дизайн интерьера: основные принципы"
  "Научные открытия 2024 года"
  "Экологические проблемы и решения"
  "Здоровый образ жизни"
  "Финансовая грамотность"
  "Психология успеха"
)

CONTENTS=(
  "В этой статье мы рассмотрим интересные аспекты современного программирования и поделимся полезными советами для разработчиков всех уровней."
  "Продуктивность - это ключ к успеху. В этом посте мы обсудим различные техники и методы, которые помогут вам работать более эффективно."
  "Веб-технологии стремительно развиваются. Давайте вместе проследим эволюцию интернета и современных фреймворков."
  "Обучение - это непрерывный процесс. Здесь вы найдете практические советы, которые помогут вам учиться быстрее и эффективнее."
  "IT-индустрия предлагает множество возможностей. Мы расскажем, с чего начать и как построить успешную карьеру в технологиях."
  "Правильные инструменты делают работу намного проще. В этом обзоре представлены лучшие инструменты для разработчиков."
  "Дизайн окружает нас повсюду. Узнайте о последних трендах и тенденциях в мире визуального дизайна."
  "Путешествия открывают новые горизонты. Поделимся впечатлениями о невероятных местах, которые стоит посетить."
  "Кулинария - это искусство. Здесь собраны рецепты, которые порадуют вас и ваших близких."
  "Спорт объединяет людей. Рассказываем о самых впечатляющих достижениях и рекордах в мире спорта."
  "Фотография позволяет запечатлеть моменты. Поделимся техниками и советами для создания потрясающих снимков."
  "Музыка меняет настроение. Обзор новых альбомов и треков, которые заслуживают внимания."
  "Кино - это окно в другой мир. Рецензии и обзоры самых интересных фильмов сезона."
  "Книги расширяют кругозор. Рекомендации литературы, которая обязательно должна быть в вашей библиотеке."
  "Интерьер формирует атмосферу. Основные принципы создания уютного и функционального пространства."
  "Наука движет прогресс. Обзор самых значимых научных открытий последнего времени."
  "Экология важна для будущего. Обсуждение актуальных экологических проблем и способов их решения."
  "Здоровье - главное богатство. Советы по поддержанию физической формы и хорошего самочувствия."
  "Финансы требуют внимания. Основы финансовой грамотности для уверенного управления личным бюджетом."
  "Психология помогает понять себя. Стратегии и техники, которые способствуют личностному росту и успеху."
)

# Функция для получения случайных категорий
get_random_categories() {
  if [ ${#CATEGORY_IDS[@]} -eq 0 ]; then
    echo "null"
    return
  fi
  
  local num_cats=$((RANDOM % 3 + 1))  # 1-3 категории
  if [ $num_cats -gt ${#CATEGORY_IDS[@]} ]; then
    num_cats=${#CATEGORY_IDS[@]}
  fi
  
  local selected=()
  local indices=()
  local available=($(seq 0 $((${#CATEGORY_IDS[@]} - 1))))
  
  # Перемешиваем индексы
  for i in "${available[@]}"; do
    indices+=("$i")
  done
  
  # Простое перемешивание индексов
  for ((i=${#indices[@]}-1; i>0; i--)); do
    j=$((RANDOM % (i+1)))
    tmp=${indices[i]}
    indices[i]=${indices[j]}
    indices[j]=$tmp
  done
  
  # Выбираем случайные категории
  for ((i=0; i<num_cats; i++)); do
    idx=${indices[i]}
    selected+=("\"${CATEGORY_IDS[idx]}\"")
  done
  
  echo "[$(IFS=,; echo "${selected[*]}")]"
}

# Создание 100 постов
echo -e "${YELLOW}Создание 100 постов...${NC}"

SUCCESS_COUNT=0
FAIL_COUNT=0

for i in {1..100}; do
  # Выбор заголовка и контента (циклически)
  TITLE_INDEX=$(((i - 1) % ${#TITLES[@]}))
  CONTENT_INDEX=$(((i - 1) % ${#CONTENTS[@]}))
  
  # Добавляем номер к заголовку для уникальности
  TITLE="${TITLES[$TITLE_INDEX]} #${i}"
  CONTENT="${CONTENTS[$CONTENT_INDEX]} Это пост номер ${i} в нашей коллекции."
  
  # Получаем случайные категории
  CATEGORIES_JSON=$(get_random_categories)
  
  # Формируем JSON body
  if [ "$CATEGORIES_JSON" = "null" ]; then
    JSON_BODY="{
      \"title\": \"${TITLE}\",
      \"content\": \"${CONTENT}\",
      \"categories\": null
    }"
  else
    JSON_BODY="{
      \"title\": \"${TITLE}\",
      \"content\": \"${CONTENT}\",
      \"categories\": ${CATEGORIES_JSON}
    }"
  fi
  
  # Создаем POST запрос
  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/posts/create" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "$JSON_BODY")
  
  HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
  BODY=$(echo "$RESPONSE" | sed '$d')
  
  if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    if [ $((i % 10)) -eq 0 ]; then
      echo -e "${GREEN}✓ Создано постов: ${i}/100${NC}"
    fi
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo -e "${RED}✗ Ошибка при создании поста #${i}: HTTP ${HTTP_CODE}${NC}"
  fi
  
  # Небольшая задержка, чтобы не перегружать API
  sleep 0.1
done

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Генерация завершена!${NC}"
echo -e "${GREEN}Успешно создано: ${SUCCESS_COUNT} постов${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
  echo -e "${YELLOW}Ошибок: ${FAIL_COUNT}${NC}"
fi
echo -e "${GREEN}═══════════════════════════════════════${NC}"

