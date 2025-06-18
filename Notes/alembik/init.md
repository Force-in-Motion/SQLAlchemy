\*\*Alembic \*\*- это инструмент для работы с миграциями для SQLAlchemy. Официальная [документация](https://alembic.sqlalchemy.org/en/latest/)

Что же он может?

1. Создавать миграции - Alembic генерирует файлы миграций, которые содержат инструкции для изменения схемы базы данных.
2. Применять миграции, т.е. изменять состояние базы до указанной ревизии.
3. Осуществлять откат миграций - мы можем вернуться к предыдущей версии схемы базы данных.
4. Отслеживать версии - Alembic автоматически отслеживает версии миграций, сохраняя информацию о применённых миграциях в специальной таблице в базе данных.
5. Поддерживает различные базы данных - PostgreSQL, MySQL, SQLite и другие.
6. Работать с несколькими окружениями - Alembic позволяет управлять миграциями в разных окружениях (например, разработка, тестирование, продакшн). Для этого настраиваются отдельные конфигурации.

Очевидно, что чем раньше мы начнём использовать миграции в своём проекте, тем проще нам будет выявлять и исправлять недостатки.

Установка библиотеки:

<pre class="code-fence" md-src-pos="1023..1055"><div class="code-fence-highlighter-copy-button" data-fence-content="cGlwIGluc3RhbGwgYWxlbWJpYw=="><img class="code-fence-highlighter-copy-button-icon" data-original-src="Notes/alembik" src="http://localhost:63342/markdownPreview/997601426/Notes/alembik?_ijt=na9s5lb3p8q6njdu2ul6ps9e59"/><span class="tooltiptext"></span></div><code class="language-cmake" md-src-pos="1023..1055"><span md-src-pos="1023..1032"></span><span md-src-pos="1032..1052">pip install alembic
</span><span md-src-pos="1052..1055"></span></code></pre>

После установки Alembic, нам нужно инициализировать его в папке проекта. Для этого перейдем в папку проекта и выполним:

<pre class="code-fence" md-src-pos="1178..1212"><div class="code-fence-highlighter-copy-button" data-fence-content="YWxlbWJpYyBpbml0IGFsZW1iaWM="><img class="code-fence-highlighter-copy-button-icon" data-original-src="Notes/alembik" src="http://localhost:63342/markdownPreview/997601426/Notes/alembik?_ijt=na9s5lb3p8q6njdu2ul6ps9e59"/><span class="tooltiptext"></span></div><code class="language-csharp" md-src-pos="1178..1212"><span md-src-pos="1178..1188"></span><span md-src-pos="1188..1209">alembic init alembic
</span><span md-src-pos="1209..1212"></span></code></pre>

<pre class="code-fence" md-src-pos="1214..1295"><div class="code-fence-highlighter-copy-button" data-fence-content="c3FsYWxjaGVteS51cmwgPSBwb3N0Z3Jlc3FsK3BzeWNvcGcyOi8vZ3NhOjA1MDJAbG9jYWxob3N0OjgwODAvUG9zdGdyZVNRTA=="><img class="code-fence-highlighter-copy-button-icon" data-original-src="Notes/alembik" src="http://localhost:63342/markdownPreview/997601426/Notes/alembik?_ijt=na9s5lb3p8q6njdu2ul6ps9e59"/><span class="tooltiptext"></span></div><code md-src-pos="1214..1295"><span md-src-pos="1214..1218"></span><span md-src-pos="1218..1292">sqlalchemy.url = postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL
</span><span md-src-pos="1292..1295"></span></code></pre>

В файле env.py импортируем все модели и указываем target\_metadata = Base.metadata

Для того чтобы миграции в папке versions располагались последовательно мы можем раскомментировать строку -

file\_template = %%(year)d\_%%(month).2d\_%%(day).2d\_%%(hour).2d%%(minute).2d-%%(rev)s\_%%(slug)s

Она будет добавлять к id и названию миграции дату и время ее создания


ОБЯЗАТЕЛЬНО в строке script_location файла alembic.ini указать правильный путь к скриптам в папке alembic

 Если терминал открыт в корне проекта и папка alembic находится в корне, то путь будет такой - script_location = ./alembic
