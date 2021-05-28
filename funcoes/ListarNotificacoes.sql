create or replace function listNotifications (p_id notificacao_pessoa.pessoa_id%type)
	returns table (
		nome pessoa.nome%type,
		mensagem notificacao.mensagem%type,
        lida notificacao_pessoa.lida%type
	) 
	language plpgsql
as $$
declare
	
begin
	return query 
		select
            pessoa.nome, notificacao.mensagem, notificacao_pessoa.lida
		from
			pessoa, notificacao_pessoa, notificacao
		where
            pessoa.id = p_id and notificacao_pessoa.pessoa_id = p_id and notificacao_pessoa.notificacao_id = notificacao.id;
    
end;
$$