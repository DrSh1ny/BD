CREATE OR REPLACE FUNCTION PostMessageOnBoard(
	idUser	bigint,
	auctionID	bigint,
	titulo		varchar,
	descricao	varchar
	)returns integer
LANGUAGE 'plpgsql'
AS $BODY$
declare
	c2 cursor(auctionID bigint) for
		select id
        from leilao
        where leilao.id=auctionID;
	idLeilao bigint;
	
begin
	--check if auction exists
    open c2(auctionID);
	fetch c2 into idLeilao;
    if (not found) then
        return -1;
    end if;
    close c2;
	insert into mensagem(titulo,descricao,leilao_id,pessoa_id,data) values (titulo,descricao,idLeilao,idUser,CURRENT_TIMESTAMP);	
	return 0;
end;
$BODY$;