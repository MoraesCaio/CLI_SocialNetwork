from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem, imagem_blob
from redesocial.mural import Mural
from PIL import Image


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

        while True:

            DB.cursor.execute(f'''
                SELECT
                    status
                FROM
                    rUser_Group
                WHERE
                    id_user = {State.usuario_atual['id_user']}
                AND
                    id_group = {cls.grupo['id_group']}
                ''')
            status = DB.cursor.fetchone()

            opcoes_grupo = [
                ['Cancelar', None],
                ['Ver foto', cls.ver_foto],
            ]

            if not status:
                opcoes_grupo.append(['Solicitar Entrada', cls.solicitar_entrada])
            elif status['status'] == 0:
                opcoes_grupo.append(['Cancelar Solicitação', cls.cancelar_solicitacao])
            elif cls.eh_visivel:
                opcoes_grupo.append(['Ver Mural', cls.ver_mural])
                opcoes_grupo.append(['Ver Membros', cls.ver_membros])
                opcoes_grupo.append(['Sair do Grupo', cls.sair_grupo])

            if cls.eh_adm():
                opcoes_grupo.append(['Ver Solicitações', cls.ver_solicitacoes])

            opcao_grupo = menu_opcoes('INTERAGIR COM GRUPO', opcoes_grupo)

            if not opcao_grupo:
                return

            opcoes_grupo[opcao_grupo][1]()

    @classmethod
    def solicitar_entrada(cls):
        DB.cursor.execute(f'''
            INSERT INTO
                rUser_Group(id_user, id_group, status)
            VALUES
                ({State.usuario_atual['id_user']}, {cls.grupo['id_group']}, 0)
            ''')
        DB.connection.commit()
        print('Solicitação enviada.')

    @classmethod
    def cancelar_solicitacao(cls):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            ''')
        DB.connection.commit()
        print('Solicitação cancelada.')

    @classmethod
    def sair_grupo(cls):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            ''')
        DB.connection.commit()
        print('Você saiu desse grupo.')

    @classmethod
    def configuracoes_grupo(cls):
        opcoes = [
            ['Voltar', None],
            ['Definir Visibilidade', cls.definir_visibilidade],
            ['Atualizar Nome', cls.atualizar_nome],
            ['Atualizar Descrição', cls.atualizar_descrição],
            ['Atualizar Imagem', cls.atualizar_imagem]
        ]

        while True:
            opcao = menu_opcoes('CONFIGURAÇÕES DE GRUPO', opcoes)
            if not opcao:
                return
            opcoes[opcao][1]()

    @classmethod
    def definir_visibilidade(cls):
        opcoes = [
            ['Cancelar'],
            ['Perfil Privado'],
            ['Perfil Público']
        ]

        while True:
            opcao = menu_opcoes('VISIBILIDADE', opcoes)

            if not opcao:
                return

            DB.cursor.execute(f'''
                UPDATE
                    tGroup
                SET
                    visibility={opcao-1}
                WHERE
                    id_group={cls.grupo["id_group"]}
                ''')
            DB.connection.commit()

            print(f'Visibilidade atualizada: {opcoes[opcao]}')

    @classmethod
    def atualizar_nome(cls):
        nome = input(f'Insira o NOME DO GRUPO com mais de 4 caracteres e menos de 255 caracteres (ou Aperte ENTER para cancelar).')

        while True:
            if not len(nome):
                return
            elif len(nome) >= 255 or len(nome) < 4:
                nome = input(f'NOME DO GRUPO inválido. Tente novamente (ou Aperte ENTER para cancelar).\n')
            else:
                DB.cursor.execute("UPDATE tGroup SET name=%s WHERE id_group=%s", (nome, cls.grupo['id_group']))
                DB.connection.commit()
                print(f'NOME DO GRUPO ATUALIZADO para: {nome}')
                return

    @classmethod
    def atualizar_descricao(cls):
        descricao = input(f'Insira sua DESCRICAO DO GRUPO com mais de 4 caracteres e menos de 255 caracteres. (ou Aperte ENTER para cancelar)')

        while True:
            if not len(descricao):
                return
            elif len(descricao) >= 255 or len(descricao) < 4:
                descricao = input(f'DESCRICAO DO GRUPO inválida. Tente novamente. (ou Aperte ENTER para cancelar)')
            else:
                DB.cursor.execute("UPDATE tGroup SET city=%s WHERE id_group=%s", (descricao, cls.grupo['id_group']))
                DB.connection.commit()
                print(f'DESCRICAO DO GRUPO ATUALIZADA para: {descricao}')
                return

    @classmethod
    def atualizar_imagem(cls):
        while True:
            path = input(f'Insira o caminho da IMAGEM DO GRUPO. (ou Aperte ENTER para cancelar)')
            if not len(path):
                return
            else:
                try:
                    Image.open(path)
                except:
                    option = input('Não foi possível carregar a IMAGEM DO GRUPO. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        img_blob = imagem_blob(State.imagem_usuario_padrao)
                        DB.cursor.execute("UPDATE tGroup SET image=%s WHERE id_group=%s", (img_blob, cls.grupo['id_group']))
                        DB.connection.commit()
                        return
                else:
                    img_blob = imagem_blob(path)
                    DB.cursor.execute("UPDATE tGroup SET image=%s WHERE id_group=%s", (img_blob, cls.grupo['id_group']))
                    DB.connection.commit()
                    return

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
            if cls.eh_adm():
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
                DB.connection.commit()
                print('Usuário removido do grupo.')

            elif opcao_membro == 3:
                # Banir / desbanir
                if status_do_membro == 3:
                    novo_status = 1  # Desbanir
                elif status_do_membro != 3:
                    novo_status = 3  # Banir

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
                DB.connection.commit()
                print('Operação realizada.')

            elif opcao_membro == 4:
                # Dar / remover admin
                if status_do_membro == 2:
                    novo_status = 1  # Remover admin
                elif status_do_membro == 1:
                    novo_status = 2  # Dar admin

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
                DB.connection.commit()
                print('Operação realizada.')

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
                DB.connection.commit()
                print('Solicitação aceita!')
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
                DB.connection.commit()
                print('Solicitação recusada.')

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
            # TODO: Checar antes se o usuário tem permissão pra postar no grupo
            Mural(cls.grupo['id_wall']).fazer_postagem()
        elif opcao_postagem > 1:
            # Interagir com uma postagem
            post_interagido = posts[opcao_postagem - 2]

            opcoes = [
                ['Voltar ao menu principal'],
                ['Ver comentários'],
            ]
            if post_interagido['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
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
                    # TODO: Checar antes se o usuário tem permissão pra postar no grupo
                    Mural(cls.grupo['id_wall']).fazer_comentario(post_interagido['id_post'])
                elif opcao > 1:
                    # Interagir com comentário
                    opcoes = [['Cancelar'], ['Ver respostas']]

                    # Só quem fez o comentário ou um administrador pode remove-lô
                    if comentarios[opcao - 2]['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
                        opcoes.append(['Remover comentário'])

                    opcao_comentario = menu_opcoes('INTERAGIR COM COMENTARIO', opcoes)
                    if opcao_comentario == 1:
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
                            # TODO: Checar antes se o usuário tem permissão pra postar no grupo
                            Mural(cls.grupo['id_wall']).fazer_resposta(comentarios[opcao - 2]['id_comment'])
                        elif opcao_resposta > 1:
                            # Interagir com resposta
                            opcoes = [['Cancelar']]

                            # Só quem postou a resposta ou um administrador pode remover
                            if respostas[opcao_resposta - 2]['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
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
                DB.connection.commit()
                print('Postagem removida.')

    @classmethod
    def eh_adm(cls):
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

    @classmethod
    def eh_visivel(cls):
        DB.cursor.execute(f'SELECT visibility FROM tUser WHERE id_user={cls.owner_user["id_user"]}')
        user = DB.cursor.fetchone()

        if int(user['visibility']) == 1:
            return True
        elif int(user['visibility']) == 0:
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
                    (status = 1 OR status = 2)
                ''')

            return True if DB.cursor.fetchone() else False
