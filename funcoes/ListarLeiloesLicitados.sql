create or replace function getLicitedAuctions (
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
		select  distinct(leilao.id), leilao.titulo, leilao.descricao
		from leilao, licitacao 
		where licitacao.leilao_id = leilao.id and licitacao.pessoa_id =p_id;
end;
$$