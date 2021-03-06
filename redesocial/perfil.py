import os
from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem, imagem_blob
from redesocial.grupo import Grupo
from redesocial.mural import Mural
from PIL import Image


class Perfil():

    owner_user = None

    @classmethod
    def __init__(cls, user):
        if type(user) == int:
            id_user = user
            DB.cursor.execute(f'SELECT * FROM tUser WHERE id_user = {id_user}')
            cls.owner_user = DB.cursor.fetchone()
        elif type(user) == dict:
            cls.owner_user = user

    @classmethod
    def ver_menu(cls):
        while True:
            print('\n---- PERFIL ----')
            print(f"Nome: {cls.owner_user['name']}")
            print(f"Cidade: {cls.owner_user['city']}")

            opcoes = [
                ['Voltar ao menu principal', None],
                ['Ver foto', cls.ver_foto],
            ]

            # Menu reduzido por conta do bloqueio: FOTO ou VOLTAR
            if cls.is_blocked_either(State.usuario_atual['id_user'], cls.owner_user['id_user']):
                print('Usuário bloqueado.')
                opcao = menu_opcoes('OPÇÕES DO PERFIL', opcoes)

                if not opcao:
                    return

                opcoes[opcao][1]()
                # ignore rest of loop
                continue

            if cls.eh_visivel() or cls.owner_user['id_user'] == State.usuario_atual['id_user']:
                opcoes.append(['Ver Amigos', cls.ver_amigos])
                opcoes.append(['Ver Grupos', cls.ver_grupos])
                opcoes.append(['Ver Mural', cls.ver_mural])

            if cls.owner_user['id_user'] == State.usuario_atual['id_user']:
                # Dono do perfil está visualizando o próprio perfil
                opcoes.append(['Ver Solicitações', cls.ver_solicitacoes])
                opcoes.append(['Configurações de Conta', cls.configuracoes_conta])

            opcao = menu_opcoes('OPÇÕES DO PERFIL', opcoes)

            if not opcao:
                return

            opcoes[opcao][1]()

    @classmethod
    def configuracoes_conta(cls):
        opcoes = [
            ['Voltar', None],
            ['Definir Visibilidade', cls.definir_visibilidade],
            ['Atualizar Nome', cls.atualizar_nome],
            ['Atualizar Cidade', cls.atualizar_cidade],
            ['Atualizar Imagem', cls.atualizar_imagem]
        ]

        while True:
            opcao = menu_opcoes('CONFIGURAÇÕES DE CONTA', opcoes)
            if not opcao:
                return
            opcoes[opcao][1]()

    @classmethod
    def definir_visibilidade(cls):
        opcoes = [
            ['Cancelar'],
            ['Perfil Privado'],
            ['Perfil Visível para Amigos'],
            ['Perfil Visível para Amigos e Amigos de amigos'],
            ['Perfil Público']
        ]

        while True:
            opcao = menu_opcoes('VISIBILIDADE', opcoes)

            if not opcao:
                return

            DB.cursor.execute(f'''
                UPDATE
                    tUser
                SET
                    visibility={opcao-1}
                WHERE
                    id_user={cls.owner_user["id_user"]}
                ''')
            DB.connection.commit()

            print(f'Visibilidade atualizada: {opcoes[opcao]}')

    @classmethod
    def atualizar_nome(cls):
        nome = input(f'Insira seu NOME com mais de 4 caracteres e menos de 255 caracteres (ou Aperte ENTER para cancelar).')

        while True:
            if not len(nome):
                return
            elif len(nome) >= 255 or len(nome) < 4:
                nome = input(f'NOME inválido. Tente novamente (ou Aperte ENTER para cancelar).\n')
            else:
                DB.cursor.execute("UPDATE tUser SET name=%s WHERE id_user=%s", (nome, cls.owner_user['id_user']))
                DB.connection.commit()
                print(f'NOME ATUALIZADO para: {nome}')
                return

    @classmethod
    def atualizar_cidade(cls):
        cidade = input(f'Insira sua CIDADE com mais de 4 caracteres e menos de 255 caracteres. (ou Aperte ENTER para cancelar)')

        while True:
            if not len(cidade):
                return
            elif len(cidade) >= 255 or len(cidade) < 4:
                cidade = input(f'CIDADE inválida. Tente novamente. (ou Aperte ENTER para cancelar)')
            else:
                DB.cursor.execute("UPDATE tUser SET city=%s WHERE id_user=%s", (cidade, cls.owner_user['id_user']))
                DB.connection.commit()
                print(f'CIDADE ATUALIZADA para: {cidade}')
                return

    @classmethod
    def atualizar_imagem(cls):
        while True:
            path = input(f'Insira o caminho da sua IMAGEM de perfil. (ou Aperte ENTER para cancelar)')
            if not len(path):
                return
            else:
                try:
                    Image.open(path)
                except:
                    option = input('Não foi possível carregar a IMAGEM. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        img_blob = imagem_blob(State.imagem_usuario_padrao)
                        DB.cursor.execute("UPDATE tUser SET image=%s WHERE id_user=%s", (img_blob, cls.owner_user['id_user']))
                        DB.connection.commit()
                        return
                else:
                    img_blob = imagem_blob(path)
                    DB.cursor.execute("UPDATE tUser SET image=%s WHERE id_user=%s", (img_blob, cls.owner_user['id_user']))
                    DB.connection.commit()
                    return

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.owner_user)

    @classmethod
    def ver_amigos(cls):

        while True:
            amigos = cls.get_amigos(cls.owner_user['id_user'])

            if amigos:
                opcoes = [['Cancelar']]

                for amigo in amigos:
                    # Checagem se são amigos mútuos só acontece em perfil de outras pessoas
                    if State.usuario_atual['id_user'] != cls.owner_user['id_user']:
                        DB.cursor.execute(f'''
                            SELECT
                                status
                            FROM
                                rUser_User
                            WHERE
                                status = 1
                            AND
                            (
                                (
                                    id_user_from = {State.usuario_atual['id_user']}
                                        AND
                                    id_user_to = {amigo['id_user']}
                                )
                                OR
                                (
                                    id_user_to = {State.usuario_atual['id_user']}
                                        AND
                                    id_user_from = {amigo['id_user']}
                                )
                            )
                            ''')
                        mutuo = True if DB.cursor.fetchone() else False
                    else:
                        mutuo = False

                    if mutuo:
                        opcoes.append([f'''{amigo['name']}, de {amigo['city']} (AMIGO MÚTUO)'''])
                    else:
                        opcoes.append([f'''{amigo['name']}, de {amigo['city']}'''])

                opcao = menu_opcoes('AMIGOS', opcoes)

                if not opcao:
                    return
                else:
                    cls.menu_usuario(amigos[opcao - 1])
            else:
                print('Esse usuário não tem amigos.')
                return

    @classmethod
    def menu_usuario(cls, usuario):
        while True:
            # Ver qual o relacionamento do usuário interagido com o usuário logado
            relacionamento = cls.get_relacionamento(usuario)

            opcoes = [
                ['Cancelar', None],
                ['Visitar Perfil', None]
            ]

            if not cls.is_blocked(user=usuario['id_user']):
                if not relacionamento:
                    # Não existe relacionamento entre os usuários
                    opcoes.append(['Solicitar Amizade', cls.solicitar_amizade])
                else:
                    # Já existe algum relacionamento entre os usuários
                    if relacionamento['status'] == 0:
                        opcoes.append(['Desfazer Solicitação de Amizade', cls.desfazer_solicitacao])
                    elif relacionamento['status'] == 1:
                        opcoes.append(['Desfazer Amizade', cls.desfazer_amizade])
                    else:  # relacionamento['status'] == 2:
                        opcoes.append(['Desbloquear', cls.desbloquear_usuario])

            # Opção de bloquear não aparece se o usuário já está bloqueado
            if (relacionamento and relacionamento['status'] != 2)\
                    or (not relacionamento):
                opcoes.append(['Bloquear', cls.bloquear])

            opcao = menu_opcoes(f'''INTERAGIR COM USUÁRIO''', opcoes)
            if not opcao:
                return

            if opcao != 0:
                if opcao == 1:
                    Perfil(usuario).ver_menu()
                elif opcao > 1:
                    opcoes[opcao][1](usuario)

                    DB.connection.commit()

    @classmethod
    def desfazer_solicitacao(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_User
            WHERE (
                id_user_from = {State.usuario_atual['id_user']}
            AND
                id_user_to = {usuario['id_user']}
            )
            OR (
                 id_user_to = {State.usuario_atual['id_user']}
            AND
                id_user_from = {usuario['id_user']}
            )
        ''')
        DB.connection.commit()
        print('Solicitaçãp desfeita!')

    @classmethod
    def solicitar_amizade(cls, usuario):
        DB.cursor.execute(f'''
            INSERT INTO
                rUser_User(id_user_from, id_user_to, status)
            VALUES
                ({State.usuario_atual['id_user']}, {usuario['id_user']}, 0)
        ''')
        DB.connection.commit()
        print('Amizade solicitada!')

    @classmethod
    def desfazer_amizade(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_User
            WHERE (
                id_user_from = {State.usuario_atual['id_user']}
            AND
                id_user_to = {usuario['id_user']}
            )
            OR (
                 id_user_to = {State.usuario_atual['id_user']}
            AND
                id_user_from = {usuario['id_user']}
            )
        ''')
        DB.connection.commit()
        print('Amizade desfeita.')

    @classmethod
    def desbloquear_usuario(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_User
            WHERE (
                id_user_from = {State.usuario_atual['id_user']}
            AND
                id_user_to = {usuario['id_user']}
            )
            OR (
                 id_user_to = {State.usuario_atual['id_user']}
            AND
                id_user_from = {usuario['id_user']}
            )
        ''')
        DB.connection.commit()
        print('Usuário desbloqueado.')

    @classmethod
    def bloquear(cls, usuario):
        if cls.get_relacionamento(usuario):
            cls.bloquear_conhecido(usuario)
        else:
            cls.bloquear_desconhecido(usuario)

        # Deletando Respostas, Comentários e Posts
        cls.deletar_conteudo(usuario)

        grupos_administrados = cls.get_grupos_administrados()
        for grupo in grupos_administrados:
            # Deletando Respostas, Comentários e Posts
            cls.deletar_conteudo_em_grupo(usuario, grupo)

            # Bloqueando usuário do grupo
            DB.cursor.execute(f'''
                UPDATE
                    rUser_Group
                SET
                    status = 3
                WHERE
                    id_group = {grupo['id_group']}
                AND
                    id_user = {usuario['id_user']}
                ''')
            DB.connection.commit()
        print('Usuário bloqueado.')

    @classmethod
    def bloquear_conhecido(cls, usuario):
        DB.cursor.execute(f'''
            UPDATE
                rUser_User
            SET
                status = 2,
                id_user_from = {State.usuario_atual['id_user']},
                id_user_to = {usuario['id_user']}
            WHERE
            (
                id_user_from = {State.usuario_atual['id_user']}
                    AND
                id_user_to = {usuario['id_user']}
            )
            OR
            (
                id_user_to = {State.usuario_atual['id_user']}
                    AND
                id_user_from = {usuario['id_user']}
            )
        ''')

        print('Bloqueio realizado com sucesso.')

    @classmethod
    def bloquear_desconhecido(cls, usuario):
        DB.cursor.execute(f'''
        INSERT INTO
            rUser_User(id_user_from, id_user_to, status)
        VALUES
            ({State.usuario_atual['id_user']}, {usuario['id_user']}, 2)
        ''')
        DB.connection.commit()
        print('Bloqueio realizado com sucesso.')

    @classmethod
    def ver_grupos(cls):
        while True:
            DB.cursor.execute(f'''
                SELECT
                    *
                FROM
                    rUser_Group
                INNER JOIN
                    tGroup
                ON
                    rUser_Group.id_group = tGroup.id_group
                WHERE
                    id_user = {cls.owner_user['id_user']}
                AND
                    tGroup.id_group NOT IN(
                        SELECT
                            id_group
                        FROM
                            rUser_Group
                        WHERE
                            id_user = {State.usuario_atual['id_user']}
                        AND
                            status = 3
                    )
                ''')
            grupos = DB.cursor.fetchall()

            if grupos:
                opcoes = [['Voltar ao menu principal']]  # + [[f'{grupo["name"]}'] for grupo in grupos]

                for grupo in grupos:
                    # Checagem de grupo mútuo só em perfil de outras pessoas
                    if State.usuario_atual['id_user'] != cls.owner_user['id_user']:
                        DB.cursor.execute(f'''
                            SELECT
                                status
                            FROM
                                rUser_Group
                            WHERE
                                (status = 1 OR status = 2)
                            AND
                                id_group = {grupo['id_group']}
                            AND
                                id_user = {State.usuario_atual['id_user']}
                            ''')
                        mutuo = True if DB.cursor.fetchone() else False
                    else:
                        mutuo = False

                    if mutuo:
                        opcoes.append([f'{grupo["name"]} (GRUPO MÚTUO)'])
                    else:
                        opcoes.append([f'{grupo["name"]}'])

                opcao = menu_opcoes('INTERAGIR COM GRUPO', opcoes)

                if not opcao:
                    return
                else:
                    Grupo(grupos[opcao - 1]).ver_menu()
            else:
                print('Esse usuário não está em nenhum grupo.')
                return

    @classmethod
    def ver_solicitacoes(cls):
        while True:
            DB.cursor.execute(f'''
                SELECT
                    *
                FROM
                    rUser_User
                INNER JOIN
                    tUser
                ON
                    rUser_User.id_user_from = tUser.id_user
                WHERE
                    id_user_to = {cls.owner_user['id_user']}
                AND
                    status = 0
                ''')

            solicitacoes = DB.cursor.fetchall()

            if solicitacoes:
                opcoes = [['Cancelar']] + [[f'{solicitacao["name"]}'] for solicitacao in solicitacoes]
                opcao = menu_opcoes('INTERAGIR COM SOLICITAÇÃO', opcoes)

                if not opcao:
                    return
                else:
                    aceita = menu_opcoes('ACEITAR SOLICITAÇÃO?', [['Cancelar'], ['Aceitar'], ['Rejeitar']])

                    if aceita == 1:
                        DB.cursor.execute(f'''
                            UPDATE
                                rUser_User
                            SET
                                status = 1
                            WHERE
                                id_user_from = {solicitacoes[opcao - 1]['id_user']}
                            AND
                                id_user_to = {cls.owner_user['id_user']}
                            ''')
                        DB.connection.commit()
                        print('Solicitação aceita!')
                    elif aceita == 2:
                        DB.cursor.execute(f'''
                            DELETE FROM
                                rUser_User
                            WHERE
                                id_user_from = {solicitacoes[opcao - 1]['id_user']}
                            AND
                                id_user_to = {cls.owner_user['id_user']}
                            AND
                                status = 0
                            ''')
                        DB.connection.commit()
                        print('Solicitação recusada.')
            else:
                print('Não há nenhuma solicitação para esse usuário.')
                return

    @classmethod
    def ver_mural(cls):
        while True:
            DB.cursor.execute(f'''
                SELECT
                    *
                FROM
                    tPost
                INNER JOIN
                    tUser
                ON
                    tPost.id_user = tUser.id_user
                WHERE
                    tPost.id_wall = {cls.owner_user['id_wall']}
                ''')

            posts = DB.cursor.fetchall()

            opcoes = [
                ['Voltar ao menu principal'],
                ['Criar postagem']
            ]

            for post in posts:
                if not cls.is_blocked_either(State.usuario_atual['id_user'], post['id_user']):
                    opcoes.append([f'-> {post["name"]}: {post["text"]}'])

            opcao = menu_opcoes('POSTS', opcoes)

            if not opcao:
                return
            elif opcao == 1:
                Mural(cls.owner_user['id_wall']).fazer_postagem()
            elif opcao > 1:
                # interação com Post
                cls.menu_post(posts[opcao - 2])

    @classmethod
    def menu_post(cls, post_interagido):
        opcoes = [
            ['Voltar ao menu principal'],
            ['Ver imagem do post'],
            ['Ver comentários'],
        ]

        if post_interagido['id_user'] == State.usuario_atual['id_user']:
            opcoes.append(['Remover postagem'])

        while True:
            opcao = menu_opcoes('MENU POST', opcoes)

            if not opcao:
                return

            elif opcao == 1:
                # Ver imagem do post
                ver_imagem(post_interagido)
            elif opcao == 2:
                # Ver comentários
                cls.ver_comentarios(post_interagido)
            elif opcao == 3:
                # Remover postagem
                DB.cursor.execute(f'''
                    DELETE FROM
                        tPost
                    WHERE
                        id_post = {post_interagido['id_post']}
                    ''')
                DB.connection.commit()
                print('Postagem removida.')
                return

    @classmethod
    def ver_comentarios(cls, post_interagido):
        while True:
            DB.cursor.execute(f'''
                SELECT
                    *
                FROM
                    tComment
                INNER JOIN
                    tUser
                ON
                    tComment.id_user = tUser.id_user
                WHERE
                    tComment.id_post = {post_interagido['id_post']}
                ''')

            comentarios = DB.cursor.fetchall()

            opcoes = [['Cancelar'], ['Comentar']]

            for comentario in comentarios:
                if not cls.is_blocked_either(State.usuario_atual['id_user'], comentario['id_user']):
                    opcoes.append([f'-> {comentario["name"]}: {comentario["text"]}'])

            opcao = menu_opcoes('COMENTARIOS', opcoes)

            if not opcao:
                return

            if opcao == 1:
                Mural(cls.owner_user['id_wall']).fazer_comentario(post_interagido['id_post'])
            elif opcao > 1:
                cls.menu_comentario(comentarios[opcao - 2])

    @classmethod
    def menu_comentario(cls, comentario):

        while True:
            opcoes = [['Cancelar'], ['Ver respostas']]

            # Só quem fez o comentário ou um administrador pode remove-lô
            if comentario['id_user'] == State.usuario_atual['id_user']:
                opcoes.append(['Remover comentário'])

            opcao = menu_opcoes('MENU COMENTARIO', opcoes)

            if not opcao:
                return
            elif opcao == 1:
                # Ver respostas
                cls.ver_respostas(comentario)
            elif opcao == 3:
                # Remover comentário
                DB.cursor.execute(f'''
                    DELETE FROM
                        tComment
                    WHERE
                        id_comment = {comentario['id_comment']}
                    ''')
                print('Comentário removido.')
                DB.connection.commit()

    @classmethod
    def ver_respostas(cls, comentario):
        while True:
            DB.cursor.execute(f'''
                SELECT
                    *
                FROM
                    tReply
                INNER JOIN
                    tUser
                ON
                    tReply.id_user = tUser.id_user
                WHERE
                    tReply.id_comment = {comentario['id_comment']}
                ''')

            respostas = DB.cursor.fetchall()

            opcoes = [['Cancelar'], ['Responder']]

            for resposta in respostas:
                if not cls.is_blocked_either(State.usuario_atual['id_user'], resposta['id_user']):
                    opcoes.append([f'-> {resposta["name"]}: {resposta["text"]}'])

            opcao = menu_opcoes('RESPOSTAS', opcoes)

            if not opcao:
                return
            elif opcao == 1:
                Mural(cls.owner_user['id_wall']).fazer_resposta(comentario['id_comment'])
            elif opcao > 1:
                cls.menu_resposta(respostas[opcao - 2])

    @classmethod
    def menu_resposta(cls, resposta):
        while True:
            # Interagir com resposta
            opcoes = [['Cancelar']]

            # Só quem postou a resposta ou um administrador pode remover
            if resposta['id_user'] == State.usuario_atual['id_user']:
                opcoes.append(['Remover resposta'])

            opcao = menu_opcoes('MENU RESPOSTA', opcoes)

            if not opcao:
                return
            elif opcao == 1:
                DB.cursor.execute(f'''
                    DELETE FROM
                        tReply
                    WHERE
                        id_reply = {resposta['id_reply']}
                    ''')
                print('Resposta removida.')
                DB.connection.commit()

    @classmethod
    def eh_visivel(cls):
        DB.cursor.execute(f'SELECT visibility FROM tUser WHERE id_user={cls.owner_user["id_user"]}')
        user = DB.cursor.fetchone()

        if int(user['visibility']) == 3:
            return True
        elif int(user['visibility']) == 2:
            friends = cls.get_amigos(cls.owner_user['id_user'])

            fof = []
            for friend in friends:
                fof += cls.get_amigos(friend['id_user'])

            if State.usuario_atual['id_user'] in [user['id_user'] for user in friends + fof]:
                return True
            else:
                return False

        elif int(user['visibility']) == 1:
            friends = cls.get_amigos(cls.owner_user['id_user'])
            if State.usuario_atual['id_user'] in [friend['id_user'] for friend in friends]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_blocked(cls, user=None):
        '''Retorna se o dono desse perfil bloqueou o usuário que está logado.'''
        if not user:
            user = cls.owner_user['id_user']

        return cls.is_blocked_generic(user, State.usuario_atual['id_user'])

    @classmethod
    def is_blocked_generic(cls, user_a, user_b):
        '''Retorna se A bloqueou B.'''
        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_User
            WHERE
                id_user_from = {user_a}
            AND
                id_user_to = {user_b}
            AND
                status = 2
            ''')
        result = DB.cursor.fetchone()

        return True if result else False

    @classmethod
    def is_blocked_either(cls, user_a, user_b):
        '''Retorna se há um bloqueio entre A e B.'''
        if cls.is_blocked_generic(user_a, user_b) or cls.is_blocked_generic(user_b, user_a):
            return True
        else:
            return False

    @classmethod
    def get_amigos(cls, user_id):
        DB.cursor.execute(f'''

            -- Amigos
            -- Os convites de amizade confirmados que essa pessoa fez
            SELECT
                *
            FROM
                tUser
            INNER JOIN
                rUser_User
            ON
                tUser.id_user = rUser_User.id_user_to
            WHERE
                status = 1
            AND
                id_user_from = {user_id}
            AND
                id_user NOT IN(
                    SELECT
                        id_user_from
                    FROM
                        rUser_User
                    WHERE
                        id_user_to = {State.usuario_atual['id_user']}
                    AND
                        status = 2
                )

            -- Os convites de amizade que essa pessoa aceitou
            UNION
            SELECT
                *
            FROM
                tUser
            INNER JOIN
                rUser_User
            ON
                tUser.id_user = rUser_User.id_user_from
            WHERE
                status = 1
            AND
                id_user_to = {user_id}
            AND
                id_user NOT IN(
                    SELECT
                        id_user_from
                    FROM
                        rUser_User
                    WHERE
                        id_user_to = {State.usuario_atual['id_user']}
                    AND
                        status = 2
                )
        ''')
        friends = DB.cursor.fetchall()
        return friends

    @classmethod
    def get_relacionamento(cls, usuario1, usuario2=None):
        if type(usuario2) != dict:
            usuario2 = State.usuario_atual

        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                rUser_User
            WHERE
                -- Lado esquerdo do relacionamento
                (
                    id_user_from = {usuario1['id_user']}
                        AND
                    id_user_to = {usuario2['id_user']}
                )
                OR
                -- Lado direito do relacionamento
                (
                    id_user_to = {usuario1['id_user']}
                        AND
                    id_user_from = {usuario2['id_user']}
                )
            ''')

        relacionamento = DB.cursor.fetchone()
        return relacionamento

    @classmethod
    def deletar_respostas(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                tReply
            WHERE
            (
                id_user={State.usuario_atual['id_user']}
                    AND
                id_wall={usuario['id_wall']}
            )
            OR
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={State.usuario_atual['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_comentarios(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                tComment
            WHERE
            (
                id_user={State.usuario_atual['id_user']}
                    AND
                id_wall={usuario['id_wall']}
            )
            OR
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={State.usuario_atual['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_posts(cls, usuario):
        DB.cursor.execute(f'''
            DELETE FROM
                tPost
            WHERE
            (
                id_user={State.usuario_atual['id_user']}
                    AND
                id_wall={usuario['id_wall']}
            )
            OR
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={State.usuario_atual['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_conteudo(cls, usuario):
        cls.deletar_respostas(usuario)
        cls.deletar_comentarios(usuario)
        cls.deletar_posts(usuario)

    @classmethod
    def deletar_respostas_em_grupo(cls, usuario, grupo):
        DB.cursor.execute(f'''
            DELETE FROM
                tReply
            WHERE
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={grupo['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_comentarios_em_grupo(cls, usuario, grupo):
        DB.cursor.execute(f'''
            DELETE FROM
                tComment
            WHERE
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={grupo['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_posts_em_grupo(cls, usuario, grupo):
        DB.cursor.execute(f'''
            DELETE FROM
                tPost
            WHERE
            (
                id_user={usuario['id_user']}
                    AND
                id_wall={grupo['id_wall']}
            )
        ''')
        DB.connection.commit()

    @classmethod
    def deletar_conteudo_em_grupo(cls, usuario, grupo):
        cls.deletar_respostas_em_grupo(usuario, grupo)
        cls.deletar_comentarios_em_grupo(usuario, grupo)
        cls.deletar_posts_em_grupo(usuario, grupo)

    @classmethod
    def get_grupos_administrados(cls):
        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                tGroup
            INNER JOIN
                rUser_Group
            ON
                tGroup.id_group = rUser_Group.id_group
            WHERE
            (
                id_user = {State.usuario_atual['id_user']}
                    AND
                status = 2
            )
        ''')

        grupos_administrados = DB.cursor.fetchall()
        return grupos_administrados
