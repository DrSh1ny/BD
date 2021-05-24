CREATE OR REPLACE FUNCTION public.SearchAuctionByDescription(
    <p_descricao leilao.descricao%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare 

begin
	
    return
        select * from leilao where descricao = p_descricao;

end;

$BODY$;
