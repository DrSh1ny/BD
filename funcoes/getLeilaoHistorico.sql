create or replace function getLeilaoHistorico(
	p_id bigint
)returns table (
	titulo varchar,
	descricao varchar,
	data timestamp
) 
language plpgsql
as $$
declare
begin
	return query
		SELECT historico.titulo, historico.descricao, historico.data_alteracao 
		FROM historico
		where leilao_id =p_id
		order by data_alteracao;
end;
$$