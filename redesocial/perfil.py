from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem


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
        print('\n---- PERFIL ----')
        print(f"Nome: {cls.owner_user['name']}")
        print(f"Cidade: {cls.owner_user['city']}")

        opcoes = [
            ['Voltar ao menu principal'],
        ]

        if cls.is_visible():
            opcoes.append(['Ver Amigos', cls.ver_amigos])
            opcoes.append(['Ver Grupos', cls.ver_grupos])
            opcoes.append(['Ver Mural', cls.ver_mural])

        if cls.owner_user['id_user'] == State.usuario_atual['id_user']:
            # Dono do perfil está visualizando o próprio perfil
            opcoes.append(['Ver Solicitações', cls.ver_solicitacoes])

        opcao = menu_opcoes('OPÇÕES DO PERFIL', opcoes)
        if opcao != 0:
            opcoes[opcao][1]()

    @classmethod
    def configuracoes_conta(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.owner_user)

    @classmethod
    def ver_amigos(cls):
        DB.cursor.execute(f'''
            -- Os convites de amizade confirmados que essa pessoa fez
            SELECT
                tUser.id_user, tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_to = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_from = {cls.owner_user['id_user']}

            UNION

            -- Os convites de amizade que essa pessoa aceitou
            SELECT
                tUser.id_user, tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_from = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_to = {cls.owner_user['id_user']}
            ''')
        amigos = DB.cursor.fetchall()

        if amigos:
            opcoes = [['Cancelar']] + [[f'''{amigo['name']}, de {amigo['city']}'''] for amigo in amigos]
            opcao = menu_opcoes('AMIGOS', opcoes)
            if opcao != 0:
                cls.interagir_com_usuario(amigos[opcao - 1]['id_user'])
        else:
            print('Esse usuário não tem amigos.')

    @classmethod
    def interagir_com_usuario(cls, id_interagido):
        # Ver qual o relacionamento do usuário interagido com o usuário logado
        print(f'id interagido:{id_interagido}')
        DB.cursor.execute(f'''
            -- Lado esquerdo do relacionamento
            SELECT
                *
            FROM
                rUser_User
            WHERE
                id_user_from = {id_interagido}
            AND
                id_user_to = {State.usuario_atual['id_user']}
            UNION

            -- Lado direito do relacionamento
            SELECT
                *
            FROM
                rUser_User
            WHERE
                id_user_to = {id_interagido}
            AND
                id_user_from = {State.usuario_atual['id_user']}

            ''')
        status_dos_usuarios = DB.cursor.fetchone()

        if not status_dos_usuarios:
            # Não existe relacionamento entre os usuários
            opcao_de_amizade = 'Solicitar Amizade'
        else:
            # Já existe algum relacionamento entre os usuários
            if status_dos_usuarios['status'] == 0:
                opcao_de_amizade = 'Desfazer Solicitação de Amizade'
            elif status_dos_usuarios['status'] == 1:
                opcao_de_amizade = 'Desfazer Amizade'
            elif status_dos_usuarios['status'] == 2:
                opcao_de_amizade = 'Desbloquear'

        opcoes = [
            ['Cancelar'],
            ['Visitar Perfil'],
            [opcao_de_amizade]
        ]

        # Opção de bloquear não aparece se o usuário já está bloqueado
        if (status_dos_usuarios and status_dos_usuarios['status'] != 2) or (
                not status_dos_usuarios):
            opcoes.append(['Bloquear'])

        opcao_usuario = menu_opcoes(f'''INTERAGIR COM USUÁRIO''', opcoes)
        if opcao_usuario != 0:
            if opcao_usuario == 1:
                Perfil(id_interagido).ver_menu()
            elif opcao_usuario == 2:
                if not status_dos_usuarios:
                    # Solicitar amizade
                    DB.cursor.execute(f'''
                        INSERT INTO
                            rUser_User(id_user_from, id_user_to, status)
                        VALUES
                            ({State.usuario_atual['id_user']}, {id_interagido}, 0)
                    ''')
                    print(f'{State.usuario_atual["id_user"]} solicitou à {"id_interagido"}')
                    DB.connection.commit()
                    print('Amizade solicitada!')
                elif status_dos_usuarios['status'] == 1:
                    # Desfazer amizade
                    DB.cursor.execute(f'''
                        DELETE FROM
                            rUser_user
                        WHERE (
                            id_user_from = {State.usuario_atual['id_user']}
                        AND
                            id_user_to = {id_interagido}
                        )
                        OR (
                             id_user_to = {State.usuario_atual['id_user']}
                        AND
                            id_user_from = {id_interagido}
                        )
                    ''')
                    DB.connection.commit()
                    print('Amizade desfeita.')
                else:
                    # Desbloquear usuário
                    DB.cursor.execute(f'''
                        DELETE FROM
                            rUser_user
                        WHERE (
                            id_user_from = {State.usuario_atual['id_user']}
                        AND
                            id_user_to = {id_interagido}
                        )
                        OR (
                             id_user_to = {State.usuario_atual['id_user']}
                        AND
                            id_user_from = {id_interagido}
                        )
                    ''')
                    DB.connection.commit()
                    print('Usuário desbloqueado.')
            elif opcao_usuario == 3:
                if status_dos_usuarios:
                    # Bloqueio quando os usuários já são amigos
                    DB.cursor.execute(f'''
                        UPDATE
                            rUser_User
                        SET
                            status = 2
                        WHERE (
                            id_user_from = {State.usuario_atual['id_user']}
                        AND
                            id_user_to = {id_interagido}
                        )
                        OR (
                             id_user_to = {State.usuario_atual['id_user']}
                        AND
                            id_user_from = {id_interagido}
                        )
                        ''')
                else:
                    # Bloqueio quando não sao amigos
                    DB.cursor.execute(f'''
                    INSERT INTO
                        rUser_User(id_user_from, id_user_to, status)
                    VALUES
                        ({State.usuario_atual['id_user']}, {id_interagido}, 2)
                    ''')
                DB.connection.commit()
                print('Usuário bloqueado.')

    @classmethod
    def ver_grupos(cls):
        DB.cursor.execute(f'''
            SELECT
                tGroup.name, status
            FROM
                rUser_Group
            INNER JOIN
                tGroup
            ON
                rUser_Group.id_group = tGroup.id_group
            WHERE
                id_user = {cls.owner_user['id_user']}
            ''')
        grupos = DB.cursor.fetchall()

        if grupos:
            opcoes = [['Voltar ao menu principal']] + [[f'{grupo["name"]}'] for grupo in grupos]
            # TODO: tratar opções do grupo
        else:
            print('Esse usuário não está em nenhum grupo.')

    @classmethod
    def ver_solicitacoes(cls):
        DB.cursor.execute(f'''
            SELECT
                tUser.id_user, tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_user.id_user_from = tUser.id_user
            WHERE
                id_user_to = {cls.owner_user['id_user']}
            ''')
        solicitacoes = DB.cursor.fetchall()

        if solicitacoes:
            opcoes = [['Cancelar']] + [[f'{solicitacao["name"]}'] for solicitacao in solicitacoes]
            opcao = menu_opcoes('INTERAGIR COM SOLICITAÇÃO', opcoes)

            if opcao != 0:
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
                    print('Solicitação aceita!')
                    DB.connection.commit()
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
                    print('Solicitação recusada.')
                    DB.connection.commit()
        else:
            print('Não há nenhuma solicitação para esse usuário.')

    @classmethod
    def ver_mural(cls):
        DB.cursor.execute(f'SELECT id_wall FROM tUser WHERE id_user = {cls.owner_user["id_user"]}')
        id_wall = DB.cursor.fetchone()['id_wall']

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
                tPost.id_wall = {id_wall}
            ''')
        posts = DB.cursor.fetchall()

        opcoes_postagem = [
            ['Voltar ao menu principal'],
            ['Criar postagem']
        ] + [[f'-> {post["name"]}: {post["text"]}'] for post in posts]
        opcao_postagem = menu_opcoes('INTERAGIR COM POSTAGEM', opcoes_postagem)

        if opcao_postagem == 1:
            pass  # TODO: criar postagem
        elif opcao_postagem > 1:
            # Interagir com uma postagem
            post_interagido = posts[opcao_postagem - 2]

            opcoes = [
                ['Voltar ao menu principal'],
                ['Ver comentários'],
            ]
            if post_interagido['id_user'] == State.usuario_atual['id_user'] or cls.owner_user['id_user'] == State.usuario_atual['id_user']:
                opcoes.append(['Remover postagem'])

            opcao = menu_opcoes('INTERAGIR COM POSTAGEM', opcoes)

            if opcao == 1:
                # Ver comentários
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

                opcoes = [['Cancelar'], ['Comentar']] + [[f'-> {comentario["name"]}: {comentario["text"]}'] for comentario in comentarios]
                opcao = menu_opcoes('INTERAGIR COM COMENTARIO', opcoes)

                if opcao == 1:
                    pass  # TODO: postar comentario
                elif opcao > 1:
                    # Interagir com comentário
                    opcoes = [['Cancelar'], ['Responder'], ['Ver respostas']]

                    # Só quem fez o comentário ou o dono do perfil pode remove-lô
                    if comentarios[opcao - 2]['id_user'] == State.usuario_atual['id_user'] or cls.owner_user['id_user'] == State.usuario_atual['id_user']:
                        opcoes.append(['Remover comentário'])

                    opcao_comentario = menu_opcoes('INTERAGIR COM COMENTARIO', opcoes)
                    if opcao_comentario == 1:
                        pass  # TODO: postar resposta
                    elif opcao_comentario == 2:
                        # Ver respostas
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
                                tReply.id_comment = {comentarios[opcao - 2]['id_comment']}
                            ''')
                        respostas = DB.cursor.fetchall()

                        opcoes_resposta = [['Cancelar'], ['Responder']] + [[f'-> {resposta["name"]}: {resposta["text"]}'] for resposta in respostas]
                        opcao_resposta = menu_opcoes('INTERAGIR COM RESPOSTA', opcoes_resposta)

                        if opcao_resposta == 1:
                            pass  # TODO: responder
                        elif opcao_resposta > 1:
                            # Interagir com resposta
                            opcoes = [['Cancelar']]

                            # Só quem postou a resposta ou o dono do perfil pode remover
                            if respostas[opcao_resposta - 2]['id_user'] == State.usuario_atual['id_user'] or cls.owner_user['id_user'] == State.usuario_atual['id_user']:
                                opcoes.append(['Remover resposta'])

                            if menu_opcoes('INTERAGIR COM RESPOSTA', opcoes) == 1:
                                DB.cursor.execute(f'''
                                    DELETE FROM
                                        tReply
                                    WHERE
                                        id_reply = {respostas[opcao_resposta - 2]['id_reply']}
                                    ''')
                                print('Resposta removida.')
                                DB.connection.commit()
                    elif opcao_comentario == 3:
                        # Remover comentário
                        DB.cursor.execute(f'''
                            DELETE FROM
                                tComment
                            WHERE
                                id_comment = {comentarios[opcao - 2]['id_comment']}
                            ''')
                        print('Comentário removido.')
                        DB.connection.commit()

            elif opcao == 2:
                # Remover postagem
                DB.cursor.execute(f'''
                    DELETE FROM
                        tPost
                    WHERE
                        id_post = {post_interagido['id_post']}
                    ''')
                print('Postagem removida.')
                DB.connection.commit()

    @classmethod
    def criar_grupo(cls):
        pass

    @classmethod
    def is_visible(cls):
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
    def get_amigos(cls, user_id):
        DB.cursor.execute(f'''
            -- Amigos
            -- Os convites de amizade confirmados que essa pessoa fez
            SELECT
                tUser.id_user
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_to = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_from = {user_id}

            -- Os convites de amizade que essa pessoa aceitou
            UNION
            SELECT
                tUser.id_user
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_from = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_to = {user_id}
        ''')
        friends = DB.cursor.fetchall()
        return friends
