from src.Models.User import User


def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql("""CREATE TABLE `user` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `user_identifier` varchar(255) NOT NULL,
        `password` varchar(255) NOT NULL,
        PRIMARY KEY(`id`),
        UNIQUE KEY `user_user_identifier` (`user_identifier`)
        ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8""")


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("""DROP TABLE `user`""")
