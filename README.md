# Game SnakeI

Описание:

 Пользователь играет за Змейку на игровом поле (плоскости). Игрок может собирать объекты, которые увеличивают змейку в длину, таким образом игра становится сложнее с каждым разом. Цель игры заработать как можно большее количество игровых баллов, избегая столкновения с самим собой или стенами игрового поля. После окончания игровое имя и результат сохраняются в папке с игрой под названием «Player rating.txt».
 
 В приложении будет доступно 2 режимы игры: 
 
 
 •	Поле ограничено стенами и игроку придётся избегать встречу с ними.
 
 •	Поле не ограничено стенами, и игрок может проходить через край, а змейка вылезет с противоположного края игрового поля.



В коде созданы функции, отвечающие за стартовый или финальный экран, скорость движения игровым персонажем (задаётся пользователем), загрузка изображений, игровой цикл, а также выход из игры, с закрытием всех процессов программы. Был создан и унаследован отдельный класс игрового персонажа, с рядом свойств, позволяющие изменять положения героя на плоскости. 




Техническое задание:
 
 1. Создать 3 функции: Стартовый и Финальное окно, а также само игровое окно.
 2. Создать класс с игровым персонажем (червячок), с которым сможет взаимодействовать пользователь.
 3. Создать текстовый файл, в котором будет храниться имя пользователя и его результат.
 4. В игре объекты могут взаимодействовать друг с другом.



 Для запуска программы требуется библиотека PyGame, а также её дополнительные модули
