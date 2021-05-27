CREATE OR REPLACE FUNCTION PeopleInAuctionBoard(
	auctionID	bigint
) returns table(
	id	bigint	
)
LANGUAGE 'plpgsql'
AS $BODY$
declare
begin
    return query 
		select
			DISTINCT mensagem.pessoa_id
		from
			mensagem
		where
			mensagem.leilao_id=auctionID;
			
end;
$BODY$;

CREATE OR REPLACE FUNCTION PeopleInAuctionLicitations(
	auctionID	bigint
) returns table(
	id	bigint	
)
LANGUAGE 'plpgsql'
AS $BODY$
declare
begin
    return query 
		select
			DISTINCT licitacao.pessoa_id
		from
			licitacao
		where
			licitacao.leilao_id=auctionID;
			
end;
$BODY$;