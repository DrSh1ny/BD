CREATE OR REPLACE FUNCTION public.SearchAuctionById(
    <p_artigo_codigo leilao.artigo_codigo%type>,

)
LANGUAGE 'plpgsql'
AS $BODY$
declare 

begin
    return
        select * from leilao where artigo_codigo = p.artigo_codigo;

end;

$BODY$;
