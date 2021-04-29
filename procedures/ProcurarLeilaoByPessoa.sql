CREATE OR REPLACE PROCEDURE public.SearchAuctionByPersonId(
    <p_pessoa_id leilao.pessoa_id%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare 

    c1 cursor for select id, descricao from leilao where pessoa_id = p_pessoa_id;
begin
	
    open c1;

    loop

    -- Return tabela

    end loop;

    close c1;

end;

$BODY$;
