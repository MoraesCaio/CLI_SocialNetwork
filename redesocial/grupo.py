from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem

class Grupo():

    grupo = None

    @classmethod
    def __init__(cls, grupo):
        if type(grupo) == int:
            id_group = grupo
            DB.cursor.execute(f'SELECT * FROM tGroup WHERE id_group = {id_group}')
            cls.grupo = DB.cursor.fetchone()
        elif type(grupo) == dict:
            cls.grupo = grupo

    @classmethod
    def ver_menu(cls):
        print(f"Nome: {cls.grupo['name']}")
        print(f"Descrição: {cls.grupo['description']}")

        cls.interagir_com_grupo(cls.grupo['id_group'])

    @classmethod
    def interagir_com_grupo(cls, id_interagido):
        # TODO: Integrar à função ver_menu e excluir essa.
        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {id_interagido}
            ''')
        status = DB.cursor.fetchone()

        opcoes_grupo = [
            ['Cancelar'],
            ['Visitar Grupo'],
            ['Ver Membros']
            ]

        if not status:
            opcoes_grupo.append(['Solicitar Entrada'])
        elif status['status'] == 0:
            opcoes_grupo.append(['Cancelar Solicitação'])
        elif (status['status'] == 1 or status['status'] == 2):
            opcoes_grupo.append(['Sair do Grupo'])

        if cls.logado_como_adm():
            opcoes_grupo.append(['Ver Solicitações'])

        opcao_grupo = menu_opcoes('INTERAGIR COM GRUPO', opcoes_grupo)

        if opcao_grupo == 1:
            cls.ver_mural()
        elif opcao_grupo == 2:
            cls.ver_membros()
        elif opcao_grupo == 3:
            if not status:
                # Solicitar entrada
                DB.cursor.execute(f'''
                    INSERT INTO
                        rUser_Group(id_user, id_group, status)
                    VALUES
                        ({State.usuario_atual['id_user']}, {id_interagido}, 0)
                    ''')
                print('Solicitação enviada.')
                DB.connection.commit()
            elif status['status'] == 0:
                # Cancelar solicitação
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {State.usuario_atual['id_user']}
                    AND
                        id_group = {id_interagido}
                    ''')
                print('Solicitação cancelada.')
                DB.connection.commit()
            elif status['status'] == 1:
                # Sair do grupo
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {State.usuario_atual['id_user']}
                    AND
                        id_group = {id_interagido}
                    ''')
                print('Você saiu desse grupo.')
                DB.connection.commit()
        elif opcao_grupo == 4:
            cls.ver_solicitacoes()

    @classmethod
    def configuracoes_grupo(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.grupo)

    @classmethod
    def ver_membros(cls):
        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                rUser_Group
            INNER JOIN
                tUser
            ON
                rUser_Group.id_user = tUser.id_user
            WHERE
                id_group = {cls.grupo['id_group']}
            AND
                (status != 0)
            ''')

        membros = DB.cursor.fetchall()
        opcoes = [['Cancelar']] + [[f'{membro["name"]}'] for membro in membros]
        opcao = menu_opcoes('INTERAGIR COM MEMBRO', opcoes)

        if opcao != 0:
            opcoes_membro = [['Cancelar'], ['Visitar Perfil']]
            if cls.logado_como_adm():
                # 1 = normal, 2 = admin, 3 = banido
                status_do_membro = membros[opcao - 1]['status']

                opcoes_membro.append(['Remover'])

                if status_do_membro == 3:
                    opcoes_membro.append(['Desbanir'])
                else:
                    opcoes_membro.append(['Banir'])
                    if status_do_membro == 1:
                        opcoes_membro.append(['Tornar Administrador'])
                    elif status_do_membro == 2:
                        opcoes_membro.append(['Tornar Usuário Normal'])
            opcao_membro = menu_opcoes('INTERAGIR COM MEMBRO', opcoes_membro)

            if opcao_membro == 1:
                # Visitar perfil
                from redesocial.perfil import Perfil
                Perfil(membros[opcao - 1]['id_user']).ver_menu()

            elif opcao_membro == 2:
                # Remover
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {membros[opcao - 1]['id_user']}
                    AND
                        id_group = {cls.grupo['id_group']}
                    ''')
                print('Usuário removido do grupo.')
                DB.connection.commit()

            elif opcao_membro == 3:
                # Banir / desbanir
                if status_do_membro == 3:
                    novo_status = 1 # Desbanir
                elif status_do_membro != 3:
                    novo_status = 3 # Banir

                DB.cursor.execute(f'''
                    UPDATE
                        rUser_Group
                    SET
                        status = {novo_status}
                    WHERE
                        id_user = {membros[opcao - 1]['id_user']}
                    AND
                        id_group = {cls.grupo['id_group']}
                    ''')
                print('Operação realizada.')
                DB.connection.commit()

            elif opcao_membro == 4:
                # Dar / remover admin
                if status_do_membro == 2:
                    novo_status = 1 # Remover admin
                elif status_do_membro == 1:
                    novo_status = 2 # Dar admin

                DB.cursor.execute(f'''
                    UPDATE
                        rUser_Group
                    SET
                        status = {novo_status}
                    WHERE
                        id_user = {membros[opcao - 1]['id_user']}
                    AND
                        id_group = {cls.grupo['id_group']}
                    ''')
                print('Operação realizada.')
                DB.connection.commit()

    @classmethod
    def ver_solicitacoes(cls):
        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                rUser_Group
            INNER JOIN
                tUser
            ON
                rUser_Group.id_user = tUser.id_user
            WHERE
                id_group = {cls.grupo['id_group']}
            AND
                status = 0
            ''')

        solicitacoes = DB.cursor.fetchall()
        opcoes = [['Cancelar']] + [[f'{solicitacao["name"]}'] for solicitacao in solicitacoes]
        opcao = menu_opcoes('INTERAGIR COM SOLICITAÇÃO', opcoes)

        if opcao != 0:
            opcao_solicitacao = menu_opcoes(
                'INTERAGIR COM SOLICITACAO',
                [['Cancelar'], ['Aceitar'], ['Recusar']]
                )

            if opcao_solicitacao == 1:
                DB.cursor.execute(f'''
                    UPDATE
                        rUser_Group
                    SET
                        status = 1
                    WHERE
                        id_user = {solicitacoes[opcao - 1]['id_user']}
                    AND
                        id_group = {cls.grupo['id_group']}
                    ''')
                print('Solicitação aceita!')
                DB.connection.commit()
            elif opcao_solicitacao == 2:
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {solicitacoes[opcao - 1]['id_user']}
                    AND
                        id_group = {cls.grupo['id_group']}
                    AND
                        status = 0
                    ''')
                print('Solicitação recusada.')
                DB.connection.commit()

    @classmethod
    def ver_mural(cls):
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
                tPost.id_wall = {cls.grupo['id_wall']}
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
            if post_interagido['id_user'] == State.usuario_atual['id_user'] or cls.logado_como_adm():
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

                    # Só quem fez o comentário ou um administrador pode remove-lô
                    if comentarios[opcao - 2]['id_user'] == State.usuario_atual['id_user'] or cls.logado_como_adm():
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

                            # Só quem postou a resposta ou um administrador pode remover
                            if respostas[opcao_resposta - 2]['id_user'] == State.usuario_atual['id_user'] or cls.logado_como_adm():
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
    def logado_como_adm(cls):
        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            AND
                status = 2
            ''')

        return True if DB.cursor.fetchone() else False