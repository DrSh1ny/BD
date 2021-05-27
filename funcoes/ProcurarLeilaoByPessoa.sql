CREATE OR REPLACE FUNCTION public.SearchAuctionByPersonId(
    <p_pessoa_id leilao.pessoa_id%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare 
begin

    return
        select * from leilao where pessoa_id = p_pessoa_id;
end;

$BODY$;
