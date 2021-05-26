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
    c1 cursor(in_auth_Token text) for
        select id
        from pessoa
        where pessoa.auth_token=in_auth_Token and CURRENT_DATE<exp_date;
    c2 cursor(artigo_id artigo.codigo%type) for
        select codigo
        from artigo
        where codigo=artigo_id;
    idNovo bigint;
	idPessoa bigint;
	codigoArtigo bigint;
begin
    --check if parameters are set
    if(p_titulo='' or p_descricao='') then
        return -1;
    end if;
	
    --check if user exists
    open c1(auth_Token);
	fetch c1 into idPessoa;
    if (not found) then
        return -2;
    end if;
    close c1;
	
    --check if product exists
    open c2(p_artigo_codigo);
	fetch c2 into codigoArtigo;
    if (not found) then
        insert into artigo values(p_artigo_codigo);
    end if;
    close c2;
	
    --check if end date after begin date
    if(p_data_fim<=p_data_inicio or p_data_inicio<=current_timestamp) then
        return -4;
    end if;
    
    update leilao
    set titulo = p_titulo, descricao = p_descricao, data_inicio = p_data_inicio, data_fim = p_data_fim, preco_inicial = p_preco_inicial, artigo_codigo = p_artigo_codigo
    where id = p_id;

	return p_id;
	
end;
$BODY$;
