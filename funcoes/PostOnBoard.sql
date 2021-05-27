CREATE OR REPLACE FUNCTION PostMessageOnBoard(
	authToken	varchar,
	auctionID	bigint,
	titulo		varchar,
	descricao	varchar
	)returns integer
LANGUAGE 'plpgsql'
AS $BODY$
declare
	c1 cursor(in_auth_Token text) for
		select id
        from pessoa
        where pessoa.auth_token=in_auth_Token and CURRENT_DATE<exp_date;
	c2 cursor(auctionID bigint) for
		select id
        from leilao
        where leilao.id=auctionID;
	idPessoa bigint;
	idLeilao bigint;
	
begin
    --check if user exists
    open c1(authToken);
	fetch c1 into idPessoa;
    if (not found) then
        return -2;
    end if;
    close c1;
	--check if auction exists
    open c2(auctionID);
	fetch c2 into idLeilao;
    if (not found) then
        return -1;
    end if;
    close c2;
	insert into mensagem(titulo,descricao,leilao_id,pessoa_id,data) values (titulo,descricao,idLeilao,idPessoa,CURRENT_TIMESTAMP);	
	return 0;
end;
$BODY$;