CREATE OR REPLACE FUNCTION createLicitation(
	p_id                bigint,
	p_value             bigint,
    p_pessoa_id         bigint,

) returns bigint
LANGUAGE 'plpgsql'
AS $BODY$
declare

    c1 cursor(in_max_preco bigint) for
        select max(preco) from licitacao where leilao_id = p_leilao_id;

    c2 cursor(data_inicial data_inicio%type, data_final data_fim%type) for
        select data_inicio, data_fim from leilao where id = p_leilao_id;


begin
	
    --check if id exists
    if(p_id == '')
        return -1;
    end if;
    --check if value is higher or lower
    if(in_max_preco >= p_value)
        return -2;
    end if;

    --check if time passed
    if(current_timestamp < data_inicial || current_timestamp > data_final)
        return -3;
    end if;
    
    insert into licitacao(preco, data, leilao_id, pessoa_id)
    values(p_value, current_timestamp, p_id, p_pessoa_id)

	return p_id;
	
end;
$BODY$;
