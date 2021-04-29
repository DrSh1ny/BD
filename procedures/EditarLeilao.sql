CREATE OR REPLACE PROCEDURE public.CreateAuction(
    <p_leilao_id leilao.id%type;
    <p_artigo_codigo leilao.artigo_codigo%type>,
    <p_preco_inicial leilao.preco_inicial%type>
    <p_titulo leilao.titulo%type>,
    <p_descricao leilao.descricao%type>,
    <p_pessoa_id leilao.pessoa_id%type>,
    <p_data_inicio leilao.data_inicio%type>,
    <p_data_fim leilao.data_fim%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare


begin


    update leilao set      where p_leilao_id = id;

    --ReturnLeilaoId
end;

$BODY$;