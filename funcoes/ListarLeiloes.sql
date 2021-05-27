create or replace function listLeiloes ()
	returns table (
		id leilao.id%type,
		descricao leilao.descricao%type
	) 
	language plpgsql
as $$
begin
	return query 
		select
			leilao.id,leilao.descricao
		from
			leilao
		where
			leilao.data_inicio<current_timestamp and leilao.data_fim>current_timestamp;
end;
$$

