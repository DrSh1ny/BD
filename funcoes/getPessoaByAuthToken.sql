CREATE OR REPLACE FUNCTION getPessoaByAuthToken(
	auth_Token         	text
) returns bigint
LANGUAGE 'plpgsql'
AS $BODY$
declare
    c1 cursor(in_auth_Token text) for
        select id
        from pessoa
        where pessoa.auth_token=in_auth_Token and CURRENT_DATE<exp_date;
	idPessoa bigint;
begin
    --check if user exists
    open c1(auth_Token);
	fetch c1 into idPessoa;
    if (not found) then
        return -1;
    end if;
    close c1;
	return idPessoa;
end;
$BODY$;
