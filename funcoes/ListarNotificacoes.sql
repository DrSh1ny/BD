create or replace function listNotifications (p_id bigint)
	returns table (
		mensagem notificacao.mensagem%type
	) 
	language plpgsql
as $$
declare
	
begin
	return query 
		select
            notificacao.mensagem
		from
			notificacao_pessoa, notificacao
		where
            notificacao_pessoa.pessoa_id = p_id and notificacao_pessoa.notificacao_id = notificacao.id and notificacao_pessoa.lida=false;
    
end;
$$