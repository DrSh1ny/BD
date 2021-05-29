DROP FUNCTION getvencedor(bigint);
create or replace function getVencedor(
	p_id bigint
)returns table (
		nome varchar,
		preco bigint,
		tempo timestamp
) 
language 'plpgsql'
as $$
declare
    c1 cursor for 
        select data_fim from leilao where leilao.id = p_id;

    tempinho timestamp;
begin

    open c1;
    fetch c1 into  tempinho;

    if(tempinho >= current_timestamp) then
        return query
            select pessoa.nome, licitacao.preco, licitacao.data, tempinho from licitacao, pessoa where 1=0;
    end if;
    close c1;

	return query
		SELECT pessoa.nome, licitacao.preco, licitacao.data, tempinho
		FROM licitacao, pessoa
		where  licitacao.pessoa_id = pessoa.id and licitacao.data = (select max(data) from licitacao);
end;
$$