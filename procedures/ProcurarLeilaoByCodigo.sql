CREATE OR REPLACE PROCEDURE public.SearchAuctionById(
    <p_artigo_codigo leilao.artigo_codigo%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare 

    c1 cursor for select id, descricao from leilao where artigo_codigo = p_artigo_codigo;
begin
	
    open c1;

    loop

    -- Return tabela

    end loop;

    close c1;

end;

$BODY$;
