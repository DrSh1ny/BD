CREATE OR REPLACE PROCEDURE public.getDetails(
    <p_leilao_id leilao.id%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare

    c1 cursor for 
        select * from leilao where id = p_leilao_id;
    
    c2 cursor for
        select * from licitacao where leilao_id = p_leilao_id;

    c3 cursor for
        select * from mensagem where leilao_id = p_leilao_id;

    c4 cursor for
        select * from historico where leilao_id = p_leilao_id

begin
	

    --Leilao Info


    --Licitacoes


    --Mensagens


    --Historico



end;

$BODY$;