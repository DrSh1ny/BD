CREATE OR REPLACE FUNCTION createAuction(
    p_artigo_codigo     artigo.codigo%type,
    p_preco_inicial     leilao.preco_inicial%type,
    p_titulo            leilao.titulo%type,
    p_descricao         leilao.descricao%type,
    p_pessoa_id         pessoa.id%type,
    p_data_inicio       leilao.data_inicio%type,
    p_data_fim          leilao.data_fim%type
) returns leilao.id%type
LANGUAGE 'plpgsql'
AS $BODY$
declare
    c1 cursor(pessoa_id bigint) for
        select id
        from pessoa
        where id=pessoa_id;
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
    open c1(p_pessoa_id);
	fetch c1 into idPessoa;
    if (not found) then
        return -2;
    end if;
    close c1;
	
    --check if product exists
    open c2(p_artigo_codigo);
	fetch c2 into codigoArtigo;
    if (not found) then
        return -3;
    end if;
    close c2;
	
    --check if end date after begin date
    if(p_data_fim<=p_data_inicio or p_data_inicio<=current_timestamp) then
        return -4;
    end if;
    
    insert into leilao(titulo,descricao,data_inicio,data_fim,preco_inicial,pessoa_id,artigo_codigo) 
	values(p_titulo,p_descricao,p_data_inicio,p_data_fim,p_preco_inicial,p_pessoa_id,p_artigo_codigo)
	returning id into idNovo;
	return idNovo;
	
end;
$BODY$;

