CREATE OR REPLACE FUNCTION markNotificationAsRead(
	idPessoa bigint
)RETURNS void
LANGUAGE 'plpgsql'
AS $BODY$
declare
	f record;
begin
	UPDATE notificacao_pessoa
	SET lida=true
	WHERE notificacao_pessoa.pessoa_id=idPessoa;	
end;
$BODY$;