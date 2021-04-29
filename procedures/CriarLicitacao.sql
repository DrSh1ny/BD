CREATE OR REPLACE PROCEDURE public.CreateLicitation(
    <p_leilao_id leilao.id%type>,
    <p_pessoa_id pessoa.id%type>,
    <preco licitacao.preco%type>,

)

LANGUAGE 'plpgsql'
AS $BODY$
declare

    v_preco licitacao.preco%type;

    cursor c1 from
        select max(preco) from licitacao where leilao_id = p_leilao_id;

    cursor c2 from
        select data_inicio, data_fim from leilao where id = p_leilao_id;


begin

    fetch c1 into v_preco;

    --Do Stuff

    
end;

$BODY$;


CREATE TABLE licitacao (
	preco	 BIGINT NOT NULL,
	data	 TIMESTAMP,
	leilao_id BIGINT,
	pessoa_id BIGINT,
	PRIMARY KEY(data,leilao_id,pessoa_id)
);