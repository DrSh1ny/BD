create or replace function listLeiloesFromKeyword (keyword text)
	returns table (
		id leilao.id%type,
		descricao leilao.descricao%type
	) 
	language plpgsql
as $$
declare
	pattern text;
begin
	pattern := '%' || keyword || '%';
	return query 
		select
			leilao.id,leilao.descricao
		from
			leilao
		where
			leilao.data_inicio<current_timestamp and leilao.data_fim>current_timestamp and (cast(leilao.artigo_codigo as varchar) ilike pattern or leilao.descricao ilike pattern);
end;
$$