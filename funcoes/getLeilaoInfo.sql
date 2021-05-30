create or replace function getLeilaoInfo(
	p_id bigint
)returns table (
		id bigint,
		titulo varchar,
		descricao varchar,
		data_inicio timestamp,
		data_fim timestamp,
		preco_inicial integer
) 
language 'plpgsql'
as $$
declare
begin
	return query
		select  cast(leilao.id as bigint), leilao.titulo, leilao.descricao, leilao.data_inicio, leilao.data_fim, leilao.preco_inicial
		from leilao 
		where leilao.id = p_id;
end;
$$