How Azerothcore Database Is Maintained By Git
==============================================================================
对于魔兽世界服务器来说, 主要包含服务器核心代码以及数据库中的数据两大部分. 服务器核心代码已经有非常成熟的 Git 作为版本控制工具. 但是数据库中的数据是如何进行版本控制的呢? Azerothcore 以及其他的开源魔兽世界模拟器的开发团队普遍采用了一种技术用 Git 来管理数据库中的数据版本. 本文就来详细的介绍一下这种技术.


Base and Update
------------------------------------------------------------------------------
数据库中的数据可以被抽象为两块, Base data (initial load) 和 Update data (incremental updates). 所有数据的历史版本都可以从 base + 上按照时间线单调递增排列的许多 update data 将数据恢复到任意一个历史版本. 这种设计跟数据库的 write ahead log 的思路是类似的. 这些 update data 中不仅包含了数据的变更, 还包含了表结构的变更 (ALTER). 这些表结构的变更全部都是 backward compatible 的. 也就是说你的表中有旧数据 (比如人物和装备数据) 和新版本的表结构是兼容的.

这些 Base 和 Update 本质上都是一个个 SQL 文件. 你只要按照顺序依次执行, 就可以将数据库恢复到任意一个历史版本.

**Base data**

azerothcore 到 2024 年为止, 已经发布了 10 个大版本了 (目前是 10.X). 每个大版本开始时, 都会把之前所有的数据合并起来做一个快照, 作为该版本的 base. 这样所有助于保持整个数据量在可控范围内. 下面我们以 2024-06-21 的一个 commit ``680c219770fb9dc77e372658e866f3be836df63c`` 为例, 来详细看看这些 base data 的内容.

这里我们来看一个例子 `data/sql/base/db_world/creature_queststarter.sql <https://github.com/azerothcore/azerothcore-wotlk/blob/680c219770fb9dc77e372658e866f3be836df63c/data/sql/base/db_world/creature_queststarter.sql>`_ 是给予任务的 NPC 和任务 ID 的对照表. 本质上它就是先 Create Table 然后 Insert Data.

你在 `data/sql/base <https://github.com/azerothcore/azerothcore-wotlk/tree/680c219770fb9dc77e372658e866f3be836df63c/data/sql/base>`_ 目录下可以看到大版本开始时的所有 Base 文件. 这个目录下只会保留当前大版本的 base 数据 (目前是 10.X). 如果你要找历史版本的 Base 文件, 你需要找到历史的 commit id 然后去对应的 commit 中找. 例如 ``data/sql/base <https://github.com/azerothcore/azerothcore-wotlk/tree/5dc6f9cf78f11b89214b9d878ec89e30d58388bc/data/sql/base>`_ 就是 2023-04-23 时 9.X 的最后一个小版本的 Base 数据. 10.X 之后这些 9.X 的 base 就会和 update 数据合并成为 10.X 的 base 了.

**Update data**

Update 则是在开发过程中, 为了修 bug 或加功能而创建的 SQL 文件. 举例来说 `data/sql/updates/db_characters/2023_05_23_00.sql <https://github.com/azerothcore/azerothcore-wotlk/blob/master/data/sql/updates/db_characters/2023_05_23_00.sql>`_ 就是一个对 characters 表进行 ALT 的修改. `data/sql/updates/db_world/2023_04_26_00.sql <https://github.com/azerothcore/azerothcore-wotlk/blob/master/data/sql/updates/db_world/2023_04_26_00.sql>`_ 就是一个添加新的 NPC 生物的修改.

你在 `data/sql/updates <https://github.com/azerothcore/azerothcore-wotlk/tree/master/data/sql/updates>`_ 目录下会看到类似 ``db_world`` 和 ``pending_db_world`` 这样的目录. 当开发者想要添加新内容时, 会将 SQL 放在 ``pending_db_world`` 目录中, 这样在本地用特定工具可以方便地进行测试. 测试通过后, 在 PR merge 到 master 时, 会有 BOT 定期将 pending 中的 SQL 重命名并合并到 ``db_world`` 中.


Update Core and Database
------------------------------------------------------------------------------
每当你用最新的服务器代码重新编译游戏核心时, 你都有可能需要更新数据库. 更新数据库的本质就是找到你的旧核心之后所有的 Update data, 然后按照顺序一一执行. 在 ``db_auth``, ``db_characters``, ``db_world`` 这三个数据库中, 都有一个 ``updates`` 表, 这个表是由自动 update 工具维护的, 用来追踪那些 Update SQL 文件执行过哪些没有执行过.

根据 `Database Keeping the Server Up-to-Date <https://www.azerothcore.org/wiki/database-keeping-the-server-up-to-date>`_ 这篇官方文档的说法, 你通过运行 ``worldserver`` 自动执行 database updater 程序时, 就会用我上面说的逻辑来一条条的执行 Update SQL 文件.


Why You Should Update Your Database More Frequently
------------------------------------------------------------------------------
官方推荐每周都要至少重新 build 核心并 update database 一次. 我们来看一个反例来了解一下在什么情况下如果不及时更新会出现什么麻烦.

10.X 的升级是 2023-04-24 发布的. 如果我们的服务器是在 2023-01-01 构建的, 而在 2023-05-16 的时候更新 (`点这里看 2023-05-16 时的 Code Base <https://github.com/azerothcore/azerothcore-wotlk/tree/87a172064ad13a42cf19a8c2a09a47af51aa2c37/data/sql>`_), 这样还来得及. 因为这个时候的 Base 还是 9.X 的 Base, Update 还能顺利更新. 但是如果你在 2024-04-14 的时候更新 (`点这里看 2024-04-14 时的 Code Base <https://github.com/azerothcore/azerothcore-wotlk/tree/53dbb769a4f01c3af350f922afdddcc1c53e3e6b/data/sql>`_), 这时的 Base 就已经是 10.X 的 Base 了, 里面的 Update 都是从 2023-04-24 时发布 10.X 之后的 Update, 那么你就会失去 2023-01-01 (你上一次构建的日期) 到 2023-04-24 (10.X 发布的日期) 之间的 Update, 这就会导致 10.X 之后的 Update 会有很大概率失败, 并且因为你丢失了数据所以会导致以后再也无法更新. 这时候你就得手动找到这些丢失的 Update SQL 文件并手动更新了 (特别是在生产服务器上做很不容易做).

虽然官方通常会在 bump 大版本之后有一段时间的缓冲期 (例如 9.X 到 10.X 给了 11 个月). 如果你错过了缓冲器的窗口, 就很有可能导致你的游戏服务器再也无法更新了.


Reference
------------------------------------------------------------------------------
- `Database Keeping the Server Up-to-Date <https://www.azerothcore.org/wiki/database-keeping-the-server-up-to-date>`_
- `azerothcore WIKI - SQL Directory <https://www.azerothcore.org/wiki/sql-directory>`_
