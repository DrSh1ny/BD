CREATE OR REPLACE FUNCTION createLicitation(
	pessoa_id	bigint,
	leilao_id	bigint,
	preco_oferecido		bigint
) returns int
LANGUAGE 'plpgsql'
AS $BODY$
declare
	aux record;
	c1 cursor(leilaoID bigint) for
		select * from leilao where id = leilaoID;
	c2 cursor(leilaoID bigint) for
        select *
		from licitacao
		where licitacao.leilao_id=leilaoID and licitacao.preco=(select max(preco) from licitacao where licitacao.leilao_id=leilaoID);
begin
	open c1(leilao_id);
	fetch c1 into aux;
	close c1;

	if(not found) then
		return -1;
	end if;

	if( aux.pessoa_id=pessoa_id) then 
		return -4;
	end if;

	if(aux.data_inicio > CURRENT_TIMESTAMP OR aux.data_fim<CURRENT_TIMESTAMP OR aux.preco_inicial>preco_oferecido) then
		return -2;
	end if;
	
	open c2(leilao_id);
	fetch c2 into aux;
	close c2;
	if(found and aux.preco>=preco_oferecido ) then 
		return -3;
	end if;
	insert into licitacao(leilao_id,pessoa_id,preco,data) values(leilao_id,pessoa_id,preco_oferecido,CURRENT_TIMESTAMP);
	return 0;
end;
$BODY$;