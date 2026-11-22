# Задание 1
bball <- read.csv("http://datasets.flowingdata.com/ppg2008.csv", header = TRUE)

head(bball)
str(bball)

bball <- bball[order(bball$PTS, decreasing = TRUE), ]

bball[1:5, c("Name", "PTS")]

row.names(bball) <- bball$Name

bball <- bball[, 2:20]


bball_matrix <- data.matrix(bball)

heatmap(bball_matrix,
        Rowv = NA, Colv = NA,
        col = cm.colors(256),
        scale = "column",
        margins = c(5, 10))

# Задание 2
install.packages("aplpack")
library(aplpack)

bball_faces <- bball[, 1:15]

faces(bball_faces, ncolors = 0)

# Высота лица - G (игры)
# Ширина лица - MIN (минуты)
# Форма лица  - PTS (очки)
# Высота рта  - FGM (попадания)
# Ширина рта  - FGA (попытки)
# Изгиб рта   - FGP (% попаданий)
# Высота глаз	- FTM (свободные)
# Ширина глаз	- FTA (попытки свободных)
# Высота носа - X3PP (% трёхочковых)
# Ширина носа - ORB (подборы в нападении)
# Ширина ушей - DRB (подборы в защите)
# Высота ушей - TRB (всего подборов)
# Высота шапки волос - FTP (% свободных)
# Ширина шапки волос - X3PM (трёхочковые)
# Форма шапки волос  - X3PA (попытки трёхочковых)

# ЗАдание 2**
crime <- read.csv("http://datasets.flowingdata.com/crimeRatesByState2005.csv",
                  sep = ",", header = TRUE)
ru <- c("США","Алабама","Аляска","Аризона","Арканзас","Калифорния","Колорадо",
        "Коннектикут","Делавэр","Округ Колумбия","Флорида","Джорджия","Гавайи",
        "Айдахо","Иллинойс","Индиана","Айова","Канзас","Кентукки","Луизиана",
        "Мэн","Мэриленд","Массачусетс","Мичиган","Миннесота","Миссисипи",
        "Миссури","Монтана","Небраска","Невада","Нью-Гемпшир","Нью-Джерси",
        "Нью-Мексико","Нью-Йорк","Северная Каролина","Северная Дакота","Огайо",
        "Оклахома","Орегон","Пенсильвания","Род-Айленд","Южная Каролина",
        "Южная Дакота","Теннесси","Техас","Юта","Вермонт","Вирджиния",
        "Вашингтон","Западная Вирджиния","Висконсин","Вайоминг")

# Берём 7 видов преступлений (колонки 2:8), без населения
crime_num <- crime[, 2:8]
row.names(crime_num) <- ru

faces(crime_num,
      labels   = ru,
      ncol.plot = 8,
      nrow.plot = 7,
      main     = "Лицо преступности в США",
      face.type  = 0,
      print.info = FALSE)


# высота лица  - убийства
# ширина лица  - изнасилования
# форма лица   - грабежи
# высота рта   - нападения с насилием
# ширина рта   - кражи со взломом
# изгиб улыбки - кражи имущества
# высота глаз  - кражи транспорта


# Задание 3
bball <- bball[,2:7]
stars(bball, flip.labels=FALSE, key.loc = c(15, 1.5))

stars(bball, flip.labels = FALSE, key.loc = c(15, 1.5), full = FALSE)

stars(bball, flip.labels = FALSE, key.loc = c(15, 1.5), draw.segments = TRUE)
