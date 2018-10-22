-- Insere dados para testar o programa rapidamente. Deve ser executado
-- somente quando todas as tabelas estão vazias.

INSERT INTO tWall VALUES (); -- 1
INSERT INTO tWall VALUES (); -- 2
INSERT INTO tWall VALUES (); -- 3
INSERT INTO tWall VALUES (); -- 4
INSERT INTO tWall VALUES (); -- 5
INSERT INTO tWall VALUES (); -- 6

INSERT INTO tUser(id_wall, name, city) VALUES (1, 'Samuel de Moura', 'João Pessoa');
INSERT INTO tUser(id_wall, name, city) VALUES (2, 'Caio Moraes', 'João Pessoa');
INSERT INTO tUser(id_wall, name, city) VALUES (3, 'Cathrine Vieau', 'São Paulo');
INSERT INTO tUser(id_wall, name, city) VALUES (4, 'Marlon Michna', 'Recife');
INSERT INTO tUser(id_wall, name, city) VALUES (5, 'Alfred Cridge', 'Acre');

-- Samuel é amigo de Caio
INSERT INTO rUser_User(id_user_from, id_user_to, status) VALUES (1, 2, 1);

-- Caio tem um pedido de amizade de Cathrine
INSERT INTO rUser_User(id_user_from, id_user_to, status) VALUES (3, 2, 0);

-- Caio bloqueou Marlon
INSERT INTO rUser_User(id_user_from, id_user_to, status) VALUES (2, 4, 2);

-- Exemplo de grupo
INSERT INTO tGroup(id_wall, name, description) VALUES (6, 'Projeto Final BD', 'Grupo do projeto de banco de dados');
INSERT INTO rUser_Group(id_user, id_group, status) VALUES (1, 1, 2); -- Samuel é admin do grupo
INSERT INTO rUser_Group(id_user, id_group, status) VALUES (2, 1, 1); -- Caio participa do grupo
INSERT INTO rUser_Group(id_user, id_group, status) VALUES (5, 1, 0); -- Alfred pediu pra entrar no grupo

-- Postagem de Samuel no grupo de BD
INSERT INTO tPost(id_user, id_wall, text) VALUES (1, 6, 'Sejam bem vindos ao grupo!');

-- Comentário de Caio à postagem anterior
INSERT INTO tComment(id_user, id_post, text) VALUES (2, 1, 'Obrigado.');

-- Resposta ao comentário de Caio
INSERT INTO tReply(id_user, id_comment, text) VALUES (1, 1, 'Disponha');
