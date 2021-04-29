CREATE OR REPLACE PROCEDURE public.CreateAuction(
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

    -- Insert
	insert into leilao values ( p_titulo, p_descricao,  p_data_inicio, p_data_fim, p_preco_inicial, p_pessoa_id, p_artigo_codigo);

    --ReturnLeilaoId
end;

$BODY$;


