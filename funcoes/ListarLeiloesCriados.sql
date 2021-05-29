create or replace function getCreatedAuctions (
	p_id bigint
)returns table (
		id int,
		titulo varchar,
		descricao varchar) 
language plpgsql
as $$
declare
	
begin
	return query 
		select leilao.id, leilao.titulo, leilao.descricao
		FROM leilao 
		where pessoa_id = p_id;
end;
$$