CREATE OR REPLACE PROCEDURE public.ListAuctions(
    <p_data leilao.data_inicio%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare


begin
	

    -- SELECT
	select id, descricao from leilao where p_data BETWEEN data_inicio and data_fim;

end;

$BODY$;

