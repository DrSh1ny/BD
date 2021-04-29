CREATE OR REPLACE PROCEDURE public.SearchAuctionByDescription(
    <p_descricao leilao.descricao%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare 

    c1 cursor for select id, descricao from leilao where descricao = p_descricao;
begin
	
    open c1;

    loop

    -- Return tabela

    end loop;

    close c1;

end;

$BODY$;
