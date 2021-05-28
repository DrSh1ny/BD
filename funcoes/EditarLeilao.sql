CREATE OR REPLACE FUNCTION editAuction(
	p_id                  bigint,
	p_titulo            text,
	p_descricao         text,
	p_data_inicio       TIMESTAMP,
	p_data_fim          TIMESTAMP,
	p_preco_inicial     bigint,
    p_artigo_codigo     bigint
) returns bigint
LANGUAGE 'plpgsql'
AS $BODY$
declare

    c1 cursor for 
        select titulo, descricao, data_inicio, data_fim, preco_inicial, artigo_codigo
        from leilao
        where p_id = id;

    v_titulo text;
    v_descricao text;
    v_data_inicio TIMESTAMP;
    v_data_fim TIMESTAMP;
    v_preco_inicial bigint;
    v_artigo_codigo bigint;

    c2 cursor(artigo_id artigo.codigo%type) for
        select codigo
        from artigo
        where codigo=artigo_id;
	codigoArtigo bigint;
begin
    --check if parameters are set
    if(p_titulo='' or p_descricao='') then
        return -1;
    end if;
	
    --check if product exists
    open c2(p_artigo_codigo);
	fetch c2 into codigoArtigo;
    if (not found) then
        insert into artigo values(p_artigo_codigo);
    end if;
    close c2;
	
    --check if end date after begin date
    if(p_data_fim<=p_data_inicio or p_data_inicio<=current_timestamp) then
        return -2;
    end if;


    --check if leilao exists and store it in historico
    open c1;
    fetch c1 into v_titulo, v_descricao, v_data_inicio, v_data_fim, v_preco_inicial, v_artigo_codigo;
	close c1;
    if(not found) then
        return -3;
    end if;

    insert into historico(data_alteracao, titulo, descricao, data_inicio, data_fim, preco_inicial, artigo_codigo, leilao_id)
    values( current_timestamp, v_titulo, v_descricao, v_data_inicio, v_data_fim, v_preco_inicial, v_artigo_codigo, id);

    update leilao
    set titulo = p_titulo, descricao = p_descricao, data_inicio = p_data_inicio, data_fim = p_data_fim, preco_inicial = p_preco_inicial, artigo_codigo = p_artigo_codigo
    where id = p_id;

	return p_id;
	
end;
$BODY$;