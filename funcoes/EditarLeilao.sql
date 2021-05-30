CREATE OR REPLACE FUNCTION editAuction(
	p_id                  bigint,
	p_titulo            text,
	p_descricao         text
) returns bigint
LANGUAGE 'plpgsql'
AS $BODY$
declare

    c1 cursor for 
        select titulo, descricao, data_inicio, data_fim, preco_inicial, artigo_codigo,pessoa_id
        from leilao
        where p_id = id;

    v_titulo text;
    v_descricao text;
    v_data_inicio TIMESTAMP;
    v_data_fim TIMESTAMP;
    v_preco_inicial bigint;
    v_artigo_codigo bigint;
    v_pessoa_id bigint;

begin
    --check if parameters are set
    if(p_titulo='' or p_descricao='') then
        return -1;
    end if;

    --check if leilao exists and store it in historico
    open c1;
    fetch c1 into v_titulo, v_descricao, v_data_inicio, v_data_fim, v_preco_inicial, v_artigo_codigo,v_pessoa_id;
	close c1;
    if(not found) then
        return -3;
    end if;

    insert into historico(data_alteracao, titulo, descricao, data_inicio, data_fim, preco_inicial, artigo_codigo, leilao_id,pessoa_id)
    values( current_timestamp, v_titulo, v_descricao, v_data_inicio, v_data_fim, v_preco_inicial, v_artigo_codigo, p_id,v_pessoa_id);

    update leilao
    set titulo = p_titulo, descricao = p_descricao
    where id = p_id;

	return p_id;
	
end;
$BODY$;