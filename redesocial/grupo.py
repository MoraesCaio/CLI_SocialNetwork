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

            opcoes_grupo = [
                ['Cancelar', None],
                ['Ver foto', cls.ver_foto],
            ]

            if not cls.eh_membro() and not cls.eh_bloqueado() and not cls.eh_solicitante():
                opcoes_grupo.append(['Solicitar Entrada', cls.solicitar_entrada])
            elif cls.eh_solicitante():
                opcoes_grupo.append(['Cancelar Solicitação', cls.cancelar_solicitacao])
            # membro ou adm
            elif cls.eh_membro():
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
        while True:
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

            if not opcao:
                return

            if opcao != 0:
                opcoes_membro = [['Cancelar', None], ['Visitar Perfil', cls.visitar_perfil]]

                # 1 = normal, 2 = admin, 3 = banido
                membro = membros[opcao - 1]

                if cls.eh_adm():
                    opcoes_membro.append(['Remover', cls.remover_membro])

                    if membro['status'] == 3:
                        opcoes_membro.append(['Desbanir', cls.alternar_banimento])
                    else:
                        opcoes_membro.append(['Banir', cls.alternar_banimento])
                        if membro['status'] == 1:
                            opcoes_membro.append(['Tornar Administrador', cls.alternar_adm])
                        elif membro['status'] == 2:
                            opcoes_membro.append(['Tornar Usuário Normal', cls.alternar_adm])

                opcao_membro = menu_opcoes('INTERAGIR COM MEMBRO', opcoes_membro)

                if not opcao_membro:
                    return
                else:
                    opcoes_membro[opcao_membro][1](membro)

    @classmethod
    def visitar_perfil(cls, membro):
        from redesocial.perfil import Perfil
        Perfil(membro['id_user']).ver_menu()

    @classmethod
    def remover_membro(cls, membro):
        DB.cursor.execute(f'''
            DELETE FROM
                rUser_Group
            WHERE
                id_user = {membro['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            ''')
        DB.connection.commit()
        print('Usuário removido do grupo.')

    @classmethod
    def alternar_banimento(cls, membro):
        if membro['status'] == 3:
            novo_status = 1  # Desbanir
        elif membro['status'] != 3:
            novo_status = 3  # Banir

        DB.cursor.execute(f'''
            UPDATE
                rUser_Group
            SET
                status = {novo_status}
            WHERE
                id_user = {membro['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            ''')

        DB.connection.commit()
        print('Operação realizada.')

    @classmethod
    def alternar_adm(cls, membro):
        # Dar / remover admin
        if membro['status'] == 2:
            novo_status = 1  # Remover admin
        elif membro['status'] == 1:
            novo_status = 2  # Dar admin

        DB.cursor.execute(f'''
            UPDATE
                rUser_Group
            SET
                status = {novo_status}
            WHERE
                id_user = {membro['id_user']}
            AND
                id_group = {cls.grupo['id_group']}
            ''')
        DB.connection.commit()
        print('Operação realizada.')

    @classmethod
    def ver_solicitacoes(cls):
        while True:
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

            if not opcao:
                return

            else:
                opcao_solicitacao = menu_opcoes(
                    'INTERAGIR COM SOLICITACAO',
                    [['Cancelar'], ['Aceitar'], ['Recusar']]
                )

                # Aceitar solicitação
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
                # Recusar solicitação
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
                    tPost.id_wall = {cls.grupo['id_wall']}
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
                if cls.eh_membro():
                    Mural(cls.grupo['id_wall']).fazer_postagem()
                else:
                    print('Você não faz parte desse grupo.')

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

        if post_interagido['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
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
                if cls.eh_membro():
                    Mural(cls.grupo['id_wall']).fazer_comentario(post_interagido['id_post'])
                else:
                    print('Você não faz parte desse grupo.')
            elif opcao > 1:
                cls.menu_comentario(comentarios[opcao - 2])

    @classmethod
    def menu_comentario(cls, comentario):

        while True:
            opcoes = [['Cancelar'], ['Ver respostas']]

            # Só quem fez o comentário ou um administrador pode remove-lô
            if comentario['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
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
                if cls.eh_membro():
                    Mural(cls.grupo['id_wall']).fazer_resposta(comentario['id_comment'])
                else:
                    print('Você não faz parte desse grupo.')
            elif opcao > 1:
                cls.menu_resposta(respostas[opcao - 2])

    @classmethod
    def menu_resposta(cls, resposta):
        while True:
            # Interagir com resposta
            opcoes = [['Cancelar']]

            # Só quem postou a resposta ou um administrador pode remover
            if resposta['id_user'] == State.usuario_atual['id_user'] or cls.eh_adm():
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
    def checar_status(cls, status, user=None):
        if type(user) == dict:
            id_user = user['id_user']
        elif user is None:
            id_user = State.usuario_atual['id_user']

        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_Group
            WHERE
                id_user = {id_user}
            AND
                id_group = {cls.grupo['id_group']}
            AND
                status = {status}
            ''')

        return True if DB.cursor.fetchone() else False

    @classmethod
    def eh_adm(cls, user=None):
        return cls.checar_status(2, user)

    @classmethod
    def eh_membro(cls, user=None):
        return cls.checar_status(2, user) or cls.checar_status(1, user)

    @classmethod
    def eh_bloqueado(cls, user=None):
        return cls.checar_status(3, user)

    @classmethod
    def eh_solicitante(cls, user=None):
        return cls.checar_status(0, user)

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
